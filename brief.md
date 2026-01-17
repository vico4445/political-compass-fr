# Political Compass FR

## Vision du projet

Créer une représentation spatiale data-driven des positions politiques en France basée sur les votes réels à l'Assemblée nationale, révélant les axes de clivage au-delà de la traditionnelle dichotomie gauche/droite.

## Objectifs

### Objectif principal
Détecter les contradictions potentielles entre discours politiques et votes effectifs en analysant les patterns de vote sur les textes législatifs.

### Objectifs secondaires
- Découvrir les axes politiques réels qui structurent le débat parlementaire français
- Visualiser les partis politiques comme des zones dans un espace multidimensionnel
- Identifier les textes qui créent des alliances inattendues
- Comprendre l'essence de chaque parti par les textes qu'ils votent

## Méthodologie

### Phase 1 : Projection basée sur les votes (approche comportementale)

**Principe** : Créer une carte spatiale où chaque point représente un texte de loi, positionné selon les patterns de vote des groupes parlementaires.

**Inputs** :
- Textes de loi votés à l'Assemblée nationale
- Résultats des votes par groupe parlementaire (pour/contre/abstention)
- Groupes parlementaires : Renaissance, LR, RN, LFI, PS, EELV, etc.

**Process** :
1. Construction d'une matrice textes × partis (qui vote quoi)
2. Application de trois techniques de projection pour comparaison :
   - **LDA (Linear Discriminant Analysis)** : maximise la séparation entre groupes parlementaires
   - **PCA** : révèle les axes de variance maximale dans les votes
   - **t-SNE/UMAP** : préserve les structures locales et clusters naturels

**Output** :
- Visualisation 2D avec chaque texte comme un point
- Couleur selon les partis qui l'ont voté
- Zones/clusters représentant les positions des partis

**Principe de séparation sémantique** :
- Deux textes sur la sécurité avec approches différentes (répressive vs préventive) doivent être éloignés
- La distance reflète la divergence dans les votes, pas seulement la thématique

### Phase 2 : Interprétation thématique (analyse de contenu)

Une fois les zones de partis identifiées :
1. Analyser le contenu textuel des lois dans chaque zone
2. Extraire les thématiques dominantes (possiblement prédéfinies : économie, sécurité, social, écologie, institutions, etc.)
3. Comprendre POURQUOI tel parti vote pour tel type de texte

**Objectif** : Donner du sens aux axes mathématiques découverts en Phase 1

### Phase 3 (future) : Comparaison discours vs votes

Comparer les positions issues des votes avec :
- Programmes électoraux
- Déclarations publiques
- Communiqués de presse

## Périmètre initial

### Données
- **Source** : API Assemblée nationale / nosdeputes.fr / data.gouv.fr
- **Période** : À définir (législature actuelle ou historique multi-législatures)
- **Types de textes** : Projets et propositions de loi votés
- **Granularité** : Groupes parlementaires (pas députés individuels)

### Limitations assumées
- Phase 1 se concentre uniquement sur les votes (pas les discours)
- Abstentions et absences à gérer méthodologiquement
- Textes unanimes nécessitent un traitement spécifique

## Stack technique

### Langage
- Python 3.x

### Librairies principales
- **Collecte de données** : requests, beautifulsoup4, pandas
- **NLP/Embeddings** : scikit-learn, transformers (CamemBERT pour le français)
- **Réduction de dimensionnalité** : scikit-learn (PCA, LDA), umap-learn, sklearn.manifold (t-SNE)
- **Visualisation** : matplotlib, seaborn, plotly (interactif)
- **Notebook** : jupyter

### Structure du projet
```
political-compass-fr/
├── brief.md                    # Ce fichier
├── requirements.txt            # Dépendances Python
├── .gitignore                  # Fichiers à ignorer
├── notebooks/
│   ├── 01_data_collection.ipynb    # Collecte et nettoyage des données
│   ├── 02_vote_matrix.ipynb        # Construction matrice de votes
│   ├── 03_projections.ipynb        # Comparaison LDA/PCA/tSNE/UMAP
│   └── 04_interpretation.ipynb     # Analyse thématique
├── data/
│   ├── raw/                    # Données brutes
│   └── processed/              # Données nettoyées
└── src/
    ├── data_collection.py      # Scripts de collecte
    ├── preprocessing.py        # Nettoyage et structuration
    ├── projection.py           # Algorithmes de projection
    └── visualization.py        # Fonctions de visualisation
```

## Questions ouvertes

1. **Pondération des votes** : Pour/contre/abstention = +1/0/-1 ou autre schéma ?
2. **Normalisation** : Comment gérer les partis qui votent moins (absences) ?
3. **Textes unanimes** : Les exclure ou les garder comme référence centrale ?
4. **Évolution temporelle** : Analyser plusieurs législatures pour voir les trajectoires ?
5. **Amendements** : Analyser au niveau amendement ou uniquement vote final ?

## Prochaines étapes

1. ✅ Initialiser le projet et créer le brief
2. 🔄 Identifier et tester l'accès aux sources de données
3. ⏳ Collecter un échantillon de données pour prototype
4. ⏳ Construire la matrice de votes
5. ⏳ Implémenter et comparer les 3 projections
6. ⏳ Visualiser et interpréter les premiers résultats

---

**Date de création** : 2026-01-17
**Auteur** : Projet d'analyse politique data-driven
