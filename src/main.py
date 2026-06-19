"""
Orchestrateur principal du pipeline scientifique.

Lance en "un clic" :
  1. chargement de la configuration externalisee (YAML) ;
  2. fixation universelle des graines ;
  3. chargement (ou generation synthetique) des donnees brutes ;
  4. nettoyage + partitionnement + standardisation ;
  5. entrainement d'un modele et export d'une figure + des metriques.

Usage :
    python -m src.main
"""
import os
import sys

import matplotlib

# TODO (complete) : backend non-interactif AVANT d'importer pyplot, pour eviter
# toute tentative d'ouverture de fenetre en environnement serveur/conteneur.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (import apres matplotlib.use)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from sklearn.metrics import mean_absolute_error, r2_score  # noqa: E402

from src.preprocessing import clean_data, split_and_scale  # noqa: E402
from src.utils import load_config, set_seed  # noqa: E402


def load_or_generate_data(config) -> pd.DataFrame:
    """Charge le CSV brut s'il existe, sinon genere un jeu synthetique.

    Cette generation rend le depot auto-suffisant : le pipeline tourne meme
    sans la donnee reelle (qui, elle, n'est jamais versionnee — cf. .gitignore).
    Remplacez simplement le fichier data/raw/ par vos vraies mesures.
    """
    raw_path = config["data"]["raw_path"]
    if os.path.exists(raw_path):
        print(f"[DATA] Lecture des donnees reelles : {raw_path}")
        return pd.read_csv(raw_path)

    print("[DATA] Aucune donnee brute trouvee -> generation synthetique.")
    n = 1000
    temperature = np.random.normal(20, 5, n)
    humidity = np.random.normal(60, 15, n)
    traffic = np.random.normal(500, 120, n)
    pm25 = (
        0.8 * traffic / 10
        + 1.5 * humidity / 10
        - 0.5 * temperature
        + np.random.normal(0, 5, n)
    )
    df = pd.DataFrame(
        {
            "temperature": temperature,
            "humidity": humidity,
            "traffic": traffic,
            "pm25": pm25,
        }
    )
    # Injection volontaire de valeurs manquantes et d'outliers pour exercer
    # le pretraitement (imputation mediane + clipping IQR).
    df.loc[df.sample(frac=0.05, random_state=1).index, "humidity"] = np.nan
    df.loc[df.sample(frac=0.01, random_state=2).index, "traffic"] *= 8
    return df


def main() -> None:
    # TODO (complete) : chargement de la configuration externalisee
    config = load_config("configs/config.yaml")

    # Fixation universelle des graines pour la reproductibilite
    set_seed(config["project"]["random_seed"])

    print("[RUN] Execution du pipeline scientifique ...")

    df_raw = load_or_generate_data(config)
    df_clean = clean_data(df_raw, config)
    X_train, X_test, y_train, y_test, _ = split_and_scale(df_clean, config)

    model = RandomForestRegressor(
        n_estimators=config["model"]["n_estimators"],
        random_state=config["project"]["random_seed"],
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"[METRIQUES] MAE = {mae:.4f} | R2 = {r2:.4f}")

    # Figure : valeurs predites vs reelles
    os.makedirs(config["output"]["figures_path"], exist_ok=True)
    fig_path = os.path.join(config["output"]["figures_path"], "predictions.png")
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.4, edgecolor="k", linewidth=0.3)
    lim = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    plt.plot(lim, lim, "r--", label="y = x")
    plt.xlabel("PM2.5 reel")
    plt.ylabel("PM2.5 predit")
    plt.title(f"Predictions (R2 = {r2:.3f})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_path, dpi=120)
    plt.close()
    print(f"[FIGURE] Sauvegardee dans : {fig_path}")
    print("[DONE] Pipeline termine.")


if __name__ == "__main__":
    main()
