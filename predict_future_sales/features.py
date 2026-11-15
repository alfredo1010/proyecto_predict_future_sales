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


# ---------------------------------------------------------------------------
# Bloque 3 (secciones 8, 9 y 10)
# ---------------------------------------------------------------------------

# Grupo de categoría (texto antes de " - " en item_category_name) -> nombre en español.
# Solo para presentar gráficas (DEC-014); item_categories.csv no se modifica.
GRUPOS_CATEGORIA_ES = {
    "PC": "Accesorios",
    "Аксессуары": "Accesorios",
    "Билеты (Цифра)": "Servicios y otros",
    "Доставка товара": "Servicios y otros",
    "Игровые консоли": "Consolas",
    "Игры": "Juegos de consola",
    "Игры Android": "Juegos digitales móviles/MAC",
    "Игры MAC": "Juegos digitales móviles/MAC",
    "Игры PC": "Juegos PC",
    "Карты оплаты": "Tarjetas de pago",
    "Карты оплаты (Кино, Музыка, Игры)": "Tarjetas de pago",
    "Кино": "Cine",
    "Книги": "Libros",
    "Музыка": "Música",
    "Подарки": "Regalos",
    "Программы": "Programas",
    "Служебные": "Servicios y otros",
    "Чистые носители (шпиль)": "Medios vírgenes",
    "Чистые носители (штучные)": "Medios vírgenes",
    "Элементы питания": "Baterías",
}


def agregar_grupo_categoria(item_categories: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una copia de ``item_categories`` con la columna ``grupo_categoria``.

    El grupo es el prefijo del nombre ruso (antes de " - ") traducido con
    ``GRUPOS_CATEGORIA_ES``. Falla si aparece un prefijo sin traducción.
    """
    resultado = item_categories.copy()
    prefijo = resultado["item_category_name"].str.split(" - ").str[0].str.strip()
    resultado["grupo_categoria"] = prefijo.map(GRUPOS_CATEGORIA_ES)
    sin_grupo = prefijo[resultado["grupo_categoria"].isna()].unique()
    if len(sin_grupo):
        raise ValueError(f"Prefijos de categoría sin grupo: {list(sin_grupo)}")
    return resultado


def matriz_mensual(
    ventas: pd.DataFrame,
    dimension: str,
    valor: str = "unidades_netas",
    ultimo_bloque: int = ULTIMO_BLOQUE_HISTORICO,
) -> pd.DataFrame:
    """Matriz ``dimension`` x mes (``date_block_num`` 0..33) para heatmaps.

    Los meses sin registros quedan en 0 (DEC-008). ``ventas`` debe contener la
    columna ``dimension`` (p. ej. ``shop_id`` o ``grupo_categoria``).
    """
    resumen = resumen_ventas(ventas, ["date_block_num", dimension])
    return (
        resumen.pivot(index=dimension, columns="date_block_num", values=valor)
        .reindex(columns=range(ultimo_bloque + 1))
        .fillna(0)
    )


def cobertura_test(test: pd.DataFrame, ventas: pd.DataFrame) -> pd.DataFrame:
    """Clasifica cada par tienda-producto de ``test`` según su historial en train.

    Categorías (excluyentes): ``par con historial`` (el par se vendió alguna vez),
    ``producto conocido, par nuevo`` (el producto se vendió en otra tienda) y
    ``producto nuevo`` (el producto nunca aparece en train). Devuelve ``test``
    con la columna ``historial``.
    """
    pares = ventas[["shop_id", "item_id"]].drop_duplicates().assign(_par=True)
    resultado = test.merge(pares, on=["shop_id", "item_id"], how="left", validate="one_to_one")
    producto_conocido = resultado["item_id"].isin(ventas["item_id"].unique())
    resultado["historial"] = "producto nuevo"
    resultado.loc[producto_conocido, "historial"] = "producto conocido, par nuevo"
    resultado.loc[resultado["_par"].fillna(False).astype(bool), "historial"] = "par con historial"
    return resultado.drop(columns="_par")


def resumen_autocorrelacion(
    serie: pd.Series, nlags: int, rezago_estacional: int | None = None
) -> dict:
    """Rezagos significativos de ACF y PACF (95 %) y prueba ADF de estacionariedad.

    Un rezago es significativo si su coeficiente cae fuera de la banda de
    confianza que dibujan ``plot_acf``/``plot_pacf``. ``rezago_estacional``
    (12 en mensual, 7 en diaria) se reporta aparte si está dentro de ``nlags``.
    """
    from statsmodels.tsa.stattools import acf, adfuller, pacf

    valores = pd.Series(serie).astype(float).to_numpy()
    nlags_pacf = min(nlags, len(valores) // 2 - 1)
    coef_acf, ic_acf = acf(valores, nlags=nlags, alpha=0.05)
    coef_pacf, ic_pacf = pacf(valores, nlags=nlags_pacf, alpha=0.05, method="ywm")
    sig_acf = [k for k in range(1, nlags + 1) if abs(coef_acf[k]) > ic_acf[k, 1] - coef_acf[k]]
    sig_pacf = [
        k for k in range(1, nlags_pacf + 1) if abs(coef_pacf[k]) > ic_pacf[k, 1] - coef_pacf[k]
    ]
    resultado = {
        "acf_rezago_1": round(float(coef_acf[1]), 2),
        "rezagos_sig_acf": ", ".join(map(str, sig_acf)) or "ninguno",
        "rezagos_sig_pacf": ", ".join(map(str, sig_pacf)) or "ninguno",
        "adf_p_valor": round(float(adfuller(valores, autolag="AIC")[1]), 3),
    }
    if rezago_estacional is not None and rezago_estacional <= nlags:
        resultado["rezago_estacional"] = rezago_estacional
        resultado["acf_estacional"] = round(float(coef_acf[rezago_estacional]), 2)
    return resultado
