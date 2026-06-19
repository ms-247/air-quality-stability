import numpy as np
import pandas as pd
import pytest

from src.preprocessing import split_and_scale


def test_split_reproducibility():
    """Verifie l'invariance du partitionnement via la graine aleatoire."""
    # Generation d'un jeu de donnees de test fictif
    df = pd.DataFrame(
        {
            "feature1": range(100),
            "feature2": range(100),
            "pm25": range(100),
        }
    )

    config = {
        "data": {"target_column": "pm25", "test_size": 0.2},
        "project": {"random_seed": 42},
        "preprocessing": {"scale_features": True},
    }

    # Deux appels successifs avec EXACTEMENT la meme configuration.
    X_train1, X_test1, _, _, _ = split_and_scale(df, config)
    X_train2, X_test2, _, _, _ = split_and_scale(df, config)

    # A graine fixee, les matrices doivent etre rigoureusement identiques.
    np.testing.assert_array_equal(X_train1, X_train2)
    np.testing.assert_array_equal(X_test1, X_test2)


def test_split_shapes():
    """Controle complementaire : coherence des dimensions du partitionnement."""
    df = pd.DataFrame(
        {
            "feature1": range(100),
            "feature2": range(100),
            "pm25": range(100),
        }
    )
    config = {
        "data": {"target_column": "pm25", "test_size": 0.2},
        "project": {"random_seed": 42},
        "preprocessing": {"scale_features": True},
    }
    X_train, X_test, y_train, y_test, _ = split_and_scale(df, config)
    assert X_train.shape[0] == 80
    assert X_test.shape[0] == 20
    assert X_train.shape[1] == 2  # 2 features (target retiree)
