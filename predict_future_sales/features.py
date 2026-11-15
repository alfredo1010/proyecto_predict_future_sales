"""Agregaciones reutilizables para el EDA y las series del proyecto.

Se esperan ventas previamente limpiadas mediante ``cargar_ventas_limpias``
(``dataset.py``). No se realizan cambios a las reglas de calidad acordadas.
Las unidades e ingresos son *netos*: las devoluciones negativas se conservan.
"""

from collections.abc import Sequence
import pandas as pd

MES_INICIAL = pd.Timestamp("2013-01-01")
ULTIMO_BLOQUE_HISTORICO = 33  # ene-2013 ... oct-2015 (train)


def preparar_ventas(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega ``ingresos = item_price * item_cnt_day`` sin mutar ``sales``.

    ``date`` debe ser datetime y las cantidades/precios deben estar limpios.
    Los ingresos negativos de las devoluciones NO se reemplazan por cero.
    """
    requeridas = {"date", "date_block_num", "shop_id", "item_id", "item_price", "item_cnt_day"}
    faltantes = requeridas.difference(sales.columns)
    if faltantes:
        raise ValueError(f"Columnas requeridas ausentes: {sorted(faltantes)}")
    if not pd.api.types.is_datetime64_any_dtype(sales["date"]):
        raise TypeError("date debe ser datetime; utiliza cargar_ventas_limpias().")
    resultado = sales.copy()
    resultado["ingresos"] = resultado["item_price"] * resultado["item_cnt_day"]
    return resultado


def _con_ingresos(ventas: pd.DataFrame) -> pd.DataFrame:
    return ventas if "ingresos" in ventas.columns else preparar_ventas(ventas)


def resumen_ventas(ventas: pd.DataFrame, dimensiones: str | Sequence[str]) -> pd.DataFrame:
    """Ventas netas y registros por dimensiones, sin completar grupos inexistentes.

    Admite dimensiones como ``shop_id``, ``item_id`` o ``date_block_num``.
    Devuelve columnas: dimensiones, ``unidades_netas``, ``ingresos_netos``, ``registros``.
    """
    dimensiones = [dimensiones] if isinstance(dimensiones, str) else list(dimensiones)
    if not dimensiones:
        raise ValueError("Es necesario proporcionar una o más dimensiones.")
    datos = _con_ingresos(ventas)
    return (
        datos.groupby(dimensiones, observed=True, dropna=False, sort=True)
        .agg(unidades_netas=("item_cnt_day", "sum"),
             ingresos_netos=("ingresos", "sum"),
             registros=("item_cnt_day", "size"))
        .reset_index()
    )


def ventas_por_periodo(ventas: pd.DataFrame, frecuencia: str = "MS") -> pd.DataFrame:
    """Totales de la cadena, con períodos sin registros rellenados con cero.

    ``frecuencia``: D (diaria), W-SUN (semanal), MS (mensual), YS (anual).
    Las semanas de los extremos y el año 2015 son períodos parciales.
    """
    if frecuencia not in {"D", "W-SUN", "MS", "YS"}:
        raise ValueError("Frecuencia permitida: D, W-SUN, MS o YS.")
    datos = _con_ingresos(ventas)
    resultado = (
        datos.resample(frecuencia, on="date")
        .agg(unidades_netas=("item_cnt_day", "sum"),
             ingresos_netos=("ingresos", "sum"),
             registros=("item_cnt_day", "size"))
        .reset_index()
        .rename(columns={"date": "periodo"})
    )
    return resultado


def ventas_mensuales_por(
    ventas: pd.DataFrame, dimensiones: str | Sequence[str] | None = None
) -> pd.DataFrame:
    """Agrega ventas a mes (`date_block_num`) y dimensiones adicionales.

    Mantiene la representación *dispersa* de pares tienda-producto-mes. Un mes
    sin registros no aparece; al crear series para ACF/PACF se debe completar
    explícitamente con 0 (ver ``serie_mensual``), evitando paneles gigantes.
    """
    extras = [] if dimensiones is None else (
        [dimensiones] if isinstance(dimensiones, str) else list(dimensiones)
    )
    extras = [x for x in extras if x != "date_block_num"]
    resultado = resumen_ventas(ventas, ["date_block_num", *extras])
    meses = resultado["date_block_num"].astype(int)
    resultado.insert(1, "fecha_mes", pd.to_datetime({
        "year": 2013 + meses // 12, "month": meses % 12 + 1, "day": 1
    }))
    return resultado


def serie_mensual(
    ventas: pd.DataFrame,
    *,
    shop_id: int | None = None,
    item_id: int | None = None,
    ultimo_bloque: int = ULTIMO_BLOQUE_HISTORICO,
) -> pd.DataFrame:
    """34 meses consecutivos, con ceros para meses sin ventas del filtro.

    Para series de tienda, producto o tienda-producto seleccionados. No crea
    el panel completo de todos los pares; es apta para ACF/PACF del bloque 3.
    """
    datos = _con_ingresos(ventas)
    if shop_id is not None:
        datos = datos.loc[datos["shop_id"] == shop_id]
    if item_id is not None:
        datos = datos.loc[datos["item_id"] == item_id]
    resultado = resumen_ventas(datos, "date_block_num").set_index("date_block_num")
    resultado = resultado.reindex(range(ultimo_bloque + 1), fill_value=0).reset_index()
    meses = resultado["date_block_num"].astype(int)
    resultado.insert(1, "fecha_mes", pd.to_datetime({
        "year": 2013 + meses // 12, "month": meses % 12 + 1, "day": 1
    }))
    return resultado
