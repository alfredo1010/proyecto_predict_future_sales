"""Carga de los datos crudos del dataset Predict Future Sales (Kaggle)."""

from pathlib import Path

from loguru import logger
import pandas as pd
import typer

from predict_future_sales.config import RAW_DATA_DIR

app = typer.Typer()

# Nombre lógico de cada tabla -> archivo CSV en data/raw/
ARCHIVOS = {
    "sales_train": "sales_train.csv",
    "items": "items.csv",
    "item_categories": "item_categories.csv",
    "shops": "shops.csv",
    "test": "test.csv",
}


def cargar_datos(raw_dir: Path = RAW_DATA_DIR) -> dict[str, pd.DataFrame]:
    """Lee los 5 CSV originales de Kaggle y los devuelve en un diccionario.

    Los datos se cargan tal como vienen (sin limpieza ni conversión de tipos;
    p. ej. `date` queda como texto dd.mm.aaaa). La limpieza se documenta en
    docs/DECISIONES.md y se aplica en etapas posteriores.

    Returns:
        dict con las claves: sales_train, items, item_categories, shops, test.
    """
    faltantes = [f for f in ARCHIVOS.values() if not (raw_dir / f).exists()]
    if faltantes:
        raise FileNotFoundError(
            f"Faltan archivos en {raw_dir}: {faltantes}. "
            "Descárgalos de Kaggle (ver README, sección 'Descargar los datos')."
        )
    return {nombre: pd.read_csv(raw_dir / archivo) for nombre, archivo in ARCHIVOS.items()}


FORMATO_FECHA = "%d.%m.%Y"  # formato original de `date` en sales_train.csv (dd.mm.aaaa)


def convertir_fecha(sales: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una copia de sales_train con `date` convertida a datetime (DEC-006).

    Usa el formato explícito dd.mm.aaaa y falla si alguna fecha no se puede convertir,
    para no introducir nulos silenciosamente.
    """
    fechas = pd.to_datetime(sales["date"], format=FORMATO_FECHA, errors="coerce")
    invalidas = int(fechas.isna().sum())
    if invalidas:
        raise ValueError(f"{invalidas} fechas no cumplen el formato {FORMATO_FECHA}.")
    return sales.assign(date=fechas)


def convertir_cantidad_entera(sales: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una copia de sales_train con `item_cnt_day` como entero (DEC-006).

    Falla si existe alguna cantidad con decimales (no serían unidades válidas).
    """
    cantidades = sales["item_cnt_day"]
    con_decimales = int((cantidades % 1 != 0).sum())
    if con_decimales:
        raise ValueError(f"{con_decimales} valores de item_cnt_day tienen decimales.")
    return sales.assign(item_cnt_day=cantidades.astype("int64"))


# Tiendas duplicadas (sección 4.c, DEC-011): id a eliminar -> id que se conserva (el presente en test.csv)
MAPEO_TIENDAS_DUPLICADAS = {0: 57, 1: 58, 11: 10}


def limpiar_sales_train(sales: pd.DataFrame) -> pd.DataFrame:
    """Aplica la limpieza acordada en la sección 4 y devuelve una copia limpia de sales_train.

    Requiere `date` ya convertida (convertir_fecha). Pasos, en orden:
    1. Elimina las filas duplicadas exactas (DEC-010).
    2. Reemplaza precios <= 0 por la mediana del precio del mismo producto en la misma tienda
       y mes; si no existe, por la mediana del producto en el mes (DEC-009).
    3. Unifica las tiendas duplicadas según MAPEO_TIENDAS_DUPLICADAS (DEC-011).

    Las devoluciones (item_cnt_day < 0) se conservan (DEC-009).
    """
    limpio = sales.drop_duplicates().reset_index(drop=True)

    invalido = limpio["item_price"] <= 0
    if invalido.any():
        validos = limpio.loc[~invalido]
        med_tienda = validos.groupby(["date_block_num", "shop_id", "item_id"])[
            "item_price"
        ].median()
        med_mes = validos.groupby(["date_block_num", "item_id"])["item_price"].median()
        filas = limpio.loc[invalido]
        reemplazo = pd.Series(
            pd.MultiIndex.from_frame(filas[["date_block_num", "shop_id", "item_id"]]).map(
                med_tienda
            ),
            index=filas.index,
        )
        reemplazo = reemplazo.fillna(
            pd.Series(
                pd.MultiIndex.from_frame(filas[["date_block_num", "item_id"]]).map(med_mes),
                index=filas.index,
            )
        )
        if reemplazo.isna().any():
            raise ValueError("No se encontró un precio de referencia para algún precio inválido.")
        limpio.loc[invalido, "item_price"] = reemplazo

    limpio["shop_id"] = limpio["shop_id"].replace(MAPEO_TIENDAS_DUPLICADAS)
    return limpio


def cargar_ventas_limpias(raw_dir: Path = RAW_DATA_DIR) -> pd.DataFrame:
    """Atajo para los bloques 2 y 3: sales_train con tipos convertidos y limpieza aplicada.

    Equivale a: cargar_datos -> convertir_cantidad_entera -> convertir_fecha -> limpiar_sales_train.
    """
    sales = cargar_datos(raw_dir)["sales_train"]
    return limpiar_sales_train(convertir_fecha(convertir_cantidad_entera(sales)))


@app.command()
def main(raw_dir: Path = RAW_DATA_DIR):
    """Verifica que los datos crudos se puedan cargar y muestra su tamaño."""
    datos = cargar_datos(raw_dir)
    for nombre, df in datos.items():
        logger.info(f"{nombre}: {df.shape[0]:,} filas x {df.shape[1]} columnas")
    logger.success("Datos crudos cargados correctamente.")


if __name__ == "__main__":
    app()
