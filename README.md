# Political Compass FR

Analyse data-driven des positions politiques en France basée sur les votes à l'Assemblée nationale.

## Objectif

Créer une représentation spatiale des partis politiques français révélant les axes de clivage réels au-delà de la dichotomie gauche/droite, en analysant les patterns de vote sur les textes législatifs.

## Approche

1. **Phase 1** : Projection spatiale basée sur les votes (qui vote quoi)
2. **Phase 2** : Interprétation thématique des zones identifiées
3. **Phase 3** : Comparaison discours vs votes (futur)

## Installation

```bash
# Cloner le projet
git clone <repo-url>
cd political-compass-fr

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Structure

```
political-compass-fr/
├── brief.md              # Documentation détaillée du projet
├── notebooks/            # Notebooks Jupyter d'analyse
│   └── 01_data_collection.ipynb
├── data/                 # Données (non versionnées)
├── src/                  # Code source Python
└── requirements.txt      # Dépendances
```

## Utilisation

Ouvrir les notebooks dans l'ordre :

```bash
jupyter notebook notebooks/01_data_collection.ipynb
```

## Documentation

Voir [brief.md](brief.md) pour la documentation complète du projet.

## License

Projet personnel d'analyse politique.
