"""
Fonctions utilitaires transverses : chargement de configuration et fixation
universelle des graines aleatoires pour garantir la reproductibilite.
"""
import os
import random
from typing import Any, Dict

import numpy as np
import yaml


def load_config(path: str) -> Dict[str, Any]:
    """Charge un fichier de configuration YAML et renvoie un dictionnaire.

    Parameters
    ----------
    path : str
        Chemin vers le fichier .yaml (ex: 'configs/config.yaml').
    """
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def set_seed(seed: int) -> None:
    """Fixe TOUTES les sources d'aleatoire pour rendre le pipeline deterministe.

    On verrouille a la fois le module `random` de Python, NumPy, et la variable
    d'environnement PYTHONHASHSEED (qui influence le hachage des structures).
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
