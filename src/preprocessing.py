"""
Module de pretraitement des donnees.

Contient :
  - clean_data       : imputation par la mediane + neutralisation des outliers (IQR)
  - split_and_scale  : partitionnement train/test reproductible + standardisation
"""
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def clean_data(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    df_clean = df.copy()
    handle_missing = config["preprocessing"]["handle_missing"]

    # 1. Gestion des valeurs manquantes
    for col in df_clean.columns:
        if df_clean[col].isnull().any():
            if handle_missing == "median":
                # TODO (complete) : calcul de la mediane puis imputation
                median_value = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(median_value)

    # 2. Gestion des valeurs aberrantes (Outliers via IQR)
    threshold = config["preprocessing"]["outlier_threshold"]
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        if col != config["data"]["target_column"]:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            # TODO (complete) : bornes de Tukey
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR

            # Application du clipping pour neutraliser les outliers
            df_clean[col] = df_clean[col].clip(lower, upper)

    return df_clean


def split_and_scale(
    df: pd.DataFrame, config: Dict[str, Any]
) -> Tuple[np.ndarray, np.ndarray, pd.Series, pd.Series, Any]:
    """Separe X/y, partitionne en train/test de maniere reproductible, puis
    standardise les features.

    Le caractere reproductible repose sur `random_state` fixe a la graine du
    projet : deux appels avec la meme config renvoient des matrices identiques.

    Returns
    -------
    X_train, X_test : np.ndarray
    y_train, y_test : pd.Series
    scaler : StandardScaler | None
    """
    target = config["data"]["target_column"]
    test_size = config["data"]["test_size"]
    seed = config["project"]["random_seed"]
    scale_features = config["preprocessing"].get("scale_features", True)

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, shuffle=True
    )

    scaler = None
    if scale_features:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
    else:
        X_train = X_train.to_numpy()
        X_test = X_test.to_numpy()

    return X_train, X_test, y_train, y_test, scaler
