"""Funciones de visualización reutilizables (bloque 3: secciones 8 y 9).

Criterios comunes: un solo eje Y por gráfica, un color por serie, escala
secuencial de un solo tono para heatmaps y cuadrícula discreta.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from predict_future_sales.config import FIGURES_DIR

COLOR_PRINCIPAL = "#2a78d6"  # serie principal (azul)
COLOR_SECUNDARIO = "#eb6834"  # segunda serie / resaltado (naranja)
COLOR_NEUTRO = "#898781"  # elementos de contexto
MAPA_SECUENCIAL = "Blues"  # heatmaps: un solo tono, claro = poco, oscuro = mucho

MESES_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def etiqueta_mes(date_block_num: int) -> str:
    """0 -> 'ene-13', 33 -> 'oct-15'."""
    return f"{MESES_ES[date_block_num % 12]}-{13 + date_block_num // 12}"


def formato_miles(ax: plt.Axes, eje: str = "y") -> None:
    """Formatea los ticks del eje con separador de miles (1,234,567)."""
    formato = FuncFormatter(lambda x, _: f"{x:,.0f}")
    (ax.yaxis if eje == "y" else ax.xaxis).set_major_formatter(formato)


def guardar_figura(fig: plt.Figure, nombre: str) -> Path:
    """Guarda la figura en ``reports/figures/<nombre>.png`` y devuelve la ruta."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    ruta = FIGURES_DIR / f"{nombre}.png"
    fig.savefig(ruta, dpi=120, bbox_inches="tight")
    return ruta


def barras_horizontales(
    ax: plt.Axes,
    etiquetas: pd.Series,
    valores: pd.Series,
    titulo: str,
    xlabel: str,
    resaltar: pd.Series | None = None,
) -> None:
    """Barras horizontales ordenadas de mayor (arriba) a menor.

    ``resaltar`` (booleana, alineada con ``valores``) pinta esas barras con el
    color secundario; el resto usa el color principal.
    """
    colores = [COLOR_PRINCIPAL] * len(valores)
    if resaltar is not None:
        colores = [COLOR_SECUNDARIO if r else COLOR_PRINCIPAL for r in resaltar]
    ax.barh(list(etiquetas), list(valores), color=colores, height=0.75)
    ax.invert_yaxis()
    ax.set(title=titulo, xlabel=xlabel)
    ax.grid(axis="y", visible=False)
    formato_miles(ax, "x")


def graficar_acf_pacf(serie: pd.Series, titulo: str, lags: int, axes=None) -> plt.Figure:
    """ACF y PACF lado a lado con bandas de confianza del 95 %.

    El número de rezagos de la PACF se limita a ``len(serie) // 2 - 1``
    (requisito de statsmodels).
    """
    if axes is None:
        fig, axes = plt.subplots(1, 2, figsize=(13, 3.4))
    else:
        fig = axes[0].figure
    lags_pacf = min(lags, len(serie) // 2 - 1)
    plot_acf(
        serie,
        lags=lags,
        ax=axes[0],
        color=COLOR_PRINCIPAL,
        vlines_kwargs={"colors": COLOR_PRINCIPAL},
    )
    plot_pacf(
        serie,
        lags=lags_pacf,
        ax=axes[1],
        method="ywm",
        color=COLOR_PRINCIPAL,
        vlines_kwargs={"colors": COLOR_PRINCIPAL},
    )
    axes[0].set(title=f"ACF — {titulo}", xlabel="Rezago")
    axes[1].set(title=f"PACF — {titulo}", xlabel="Rezago")
    return fig
