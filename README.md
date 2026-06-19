# Air Quality — Projet Scientifique Reproductible & Stabilité Numérique

TP 1 & 2 — Module *Science des Données et Calcul Scientifique Avancé* (D1, 2026).

Ce dépôt illustre deux volets : (1) l'ingénierie de la reproductibilité d'un
pipeline Python (environnement isolé, configuration externalisée, tests
automatisés, versionnement propre) et (2) l'étude de la stabilité numérique en
algèbre linéaire (arithmétique IEEE 754, conditionnement, factorisation).

## Architecture

```
air-quality-stability/
├── environment.yml          # dépendances conda/mamba
├── .gitignore               # exclusion caches + données brutes
├── README.md
├── configs/
│   └── config.yaml          # hyperparamètres externalisés
├── src/
│   ├── utils.py             # load_config, set_seed
│   ├── preprocessing.py     # clean_data (médiane + IQR), split_and_scale
│   ├── main.py              # orchestrateur "un clic"
│   └── stability/           # exercices de stabilité numérique
│       ├── exercice_6_1_sommation.py
│       ├── exercice_6_2_conditionnement.py
│       └── exercice_6_3_inversion.py
├── tests/
│   └── test_preprocessing.py
├── data/                    # données NON versionnées (cf. .gitignore)
│   ├── raw/.gitkeep
│   └── processed/.gitkeep
└── reports/
    └── figures/.gitkeep
```

## Installation de l'environnement

```bash
# Création de l'environnement à partir du fichier YAML
mamba env create -f environment.yml      # (ou: conda env create -f environment.yml)

# Activation
mamba activate air_quality_stability     # (ou: conda activate air_quality_stability)
```

## Commande unique d'exécution

Depuis la racine du projet, environnement activé :

```bash
python -m src.main && python -m pytest -v
```

Cette commande **(1)** lance l'intégralité du pipeline (chargement de la
configuration, nettoyage, partitionnement, entraînement, export de la figure
`reports/figures/predictions.png` et affichage des métriques) puis **(2)**
exécute la suite de tests unitaires.

> Si aucune donnée réelle n'est présente dans `data/raw/`, un jeu de données
> synthétique est généré automatiquement afin que le pipeline reste exécutable
> de bout en bout. Déposez votre `air_quality.csv` dans `data/raw/` pour
> utiliser vos vraies mesures.

## Exécuter les exercices de stabilité numérique

```bash
python -m src.stability.exercice_6_1_sommation
python -m src.stability.exercice_6_2_conditionnement
python -m src.stability.exercice_6_3_inversion
```
