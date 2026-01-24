import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# ===============================
# Configuración de columnas
# ===============================

TARGET = "Delayed"

CAT_COLS = [
    "Marketing_Airline_Network",
    "OriginCityName",
    "DestCityName"
]

CYCLIC_COLS = {
    "DayofWeek": 7,
    "Month": 12,
    "CRSDepTime": 1440
}

NUM_COLS = ["Distance"]
BOOL_COLS = ["Holidays"]

# ===============================
# Funciones auxiliares
# ===============================

def add_cyclic_features(df: pd.DataFrame, cyclic_cols: dict) -> pd.DataFrame:
    df = df.copy()

    for col, period in cyclic_cols.items():
        df[f"{col}_sin"] = np.sin(2 * np.pi * df[col] / period)
        df[f"{col}_cos"] = np.cos(2 * np.pi * df[col] / period)

    df = df.drop(columns=list(cyclic_cols.keys()))
    return df

# ===============================
# Encoders
# ===============================

class CyclicEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, cyclic_cols: dict):
        self.cyclic_cols = cyclic_cols

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return add_cyclic_features(X, self.cyclic_cols)


class TargetEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, cols, smoothing=20):
        self.cols = cols
        self.smoothing = smoothing

    def fit(self, X, y):
        X = X.copy()
        y = y.copy()

        self.global_mean_ = y.mean()
        self.encoding_ = {}

        for col in self.cols:
            stats = (
                pd.concat([X[col], y], axis=1)
                .groupby(col)[y.name]
                .agg(["mean", "count"])
            )

            smooth = (
                (stats["count"] * stats["mean"] +
                 self.smoothing * self.global_mean_)
                / (stats["count"] + self.smoothing)
            )

            self.encoding_[col] = smooth

        return self

    def transform(self, X):
        X = X.copy()

        for col in self.cols:
            X[col] = (
                X[col]
                .map(self.encoding_[col])
                .fillna(self.global_mean_)
            )

        return X
