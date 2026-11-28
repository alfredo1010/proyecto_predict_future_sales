"""Transformadores propios compatibles con sklearn para el pipeline de preprocesamiento (Proyecto 2).

Se definen en un módulo del paquete (y no dentro del notebook) para que el archivo ``.pkl`` del pipeline
se pueda cargar desde cualquier notebook: ``pickle``/``joblib`` guardan la ruta de la clase, no su código.
Todos siguen la interfaz de sklearn: ``fit`` aprende (si aplica) y ``transform`` aplica lo aprendido.
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class Mapper(BaseEstimator, TransformerMixin):
    """Crea columnas nuevas traduciendo los valores de una columna con un diccionario fijo.

    ``mapeos`` = {columna_nueva: (columna_origen, diccionario)}. Los valores sin traducción quedan
    nulos (los rellena el imputador categórico). No aprende nada de los datos.
    """

    def __init__(self, mapeos: dict):
        self.mapeos = mapeos

    def fit(self, X, y=None):
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        check_is_fitted(self, "feature_names_in_")
        resultado = X.copy()
        for nueva, (origen, diccionario) in self.mapeos.items():
            resultado[nueva] = resultado[origen].map(diccionario).astype(object)
        return resultado

    def get_feature_names_out(self, input_features=None):
        return np.asarray([*self.feature_names_in_, *self.mapeos], dtype=object)


class IndicadorNulo(BaseEstimator, TransformerMixin):
    """Agrega una bandera 0/1 que vale 1 cuando ``columna`` es nula (antes de imputarla)."""

    def __init__(self, columna: str, nombre: str):
        self.columna = columna
        self.nombre = nombre

    def fit(self, X, y=None):
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        check_is_fitted(self, "feature_names_in_")
        return X.assign(**{self.nombre: X[self.columna].isna().astype("int8")})

    def get_feature_names_out(self, input_features=None):
        return np.asarray([*self.feature_names_in_, self.nombre], dtype=object)


class ImputadorMedianaPorGrupo(BaseEstimator, TransformerMixin):
    """Rellena la primera columna con la mediana de su grupo (segunda columna), aprendida en ``fit``.

    Si el grupo no se vio en el ajuste, usa la mediana global. Devuelve solo la columna imputada.
    """

    def fit(self, X, y=None):
        valor, grupo = X.columns[:2]
        self.columna_ = valor
        self.medianas_ = X.groupby(grupo)[valor].median().dropna().to_dict()
        self.mediana_global_ = float(X[valor].median())
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        check_is_fitted(self, "medianas_")
        valor, grupo = X.columns[:2]
        respaldo = X[grupo].map(self.medianas_).astype("float64").fillna(self.mediana_global_)
        return X[valor].astype("float64").fillna(respaldo).to_frame(valor)

    def get_feature_names_out(self, input_features=None):
        return np.asarray([self.columna_], dtype=object)


class TopeCuantil(BaseEstimator, TransformerMixin):
    """Limita cada columna por arriba en el cuantil ``cuantil`` aprendido en ``fit`` (tratamiento de outliers)."""

    def __init__(self, cuantil: float = 0.999):
        self.cuantil = cuantil

    def fit(self, X, y=None):
        self.topes_ = X.quantile(self.cuantil).to_dict()
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        check_is_fitted(self, "topes_")
        return X.clip(upper=pd.Series(self.topes_), axis=1)

    def get_feature_names_out(self, input_features=None):
        return self.feature_names_in_


class CodificadorFrecuencia(BaseEstimator, TransformerMixin):
    """Reemplaza cada categoría por su proporción de filas en el ajuste; categorías nuevas -> 0."""

    def fit(self, X, y=None):
        self.frecuencias_ = {c: X[c].value_counts(normalize=True).to_dict() for c in X.columns}
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        check_is_fitted(self, "frecuencias_")
        return pd.DataFrame(
            {c: X[c].map(self.frecuencias_[c]).astype("float64").fillna(0.0) for c in X.columns},
            index=X.index,
        )

    def get_feature_names_out(self, input_features=None):
        return np.asarray([f"{c}_frecuencia" for c in self.feature_names_in_], dtype=object)
