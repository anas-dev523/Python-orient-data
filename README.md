## Analyse des accidents corporels de la circulation

Ce dépôt présente une petite étude exploratoire sur le jeu de données public disponible sur data.gouv.fr intitulé **Base de données des accidents corporels de la circulation**. Le but est de mettre en pratique les manipulations de données vues en cours (chargement, nettoyage, statistiques descriptives et visualisations) à l'aide de Python, pandas et Plotly.

### Contenu du dépôt :

```
projet-accidents/
├── data/
│   └── accidents_insee.csv      # jeu de données brut (extrait du fichier ZIP)
├── outputs/
│   ├── 01_top_dep_accidents.html    # graphique interactif : top des départements
│   ├── 02_distribution_ttue.html    # graphique interactif : distribution des tués
│   ├── 03_scatter_geo.html          # graphique interactif : carte des accidents
│   └── clean_accidents_insee.csv    # jeu de données nettoyé
├── main.py                    # script Python d'analyse
└── requirements.txt           # dépendances Python
```

### Jeu de données

Le fichier `accidents_insee.csv` provient de la plateforme [data.gouv.fr](https://www.data.gouv.fr/) et recense les accidents corporels de la circulation. Chaque ligne représente un accident et comporte diverses informations telles que le département (`dep`), le nombre de personnes tuées (`ttue`), blessées graves (`tbg`), légères (`tbl`), les coordonnées GPS (`lat`, `long`), etc.

Colonne	   Signification simple
ttue	      nombre de personnes tuées
tbg	      blessés graves
tbl	      blessés légers
tindm	      indemnes
nbimplique	nombre de véhicules impliqués

### Exécution du projet

1. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

2. **Exécuter l'analyse :**

   ```bash
   python main.py
   ```

Le script affichera quelques statistiques dans la console, générera trois graphiques interactifs au format HTML dans le dossier `outputs` et créera un fichier CSV nettoyé.

### Résultats produits

- **01_top_dep_accidents.html** : un diagramme en barres montrant les 15 départements comptant le plus grand nombre d'accidents.
- **02_distribution_ttue.html** : un histogramme représentant la distribution du nombre de tués par accident.
- **03_scatter_geo.html** : un nuage de points positionnant chaque accident selon ses coordonnées GPS (latitude et longitude).

Ces fichiers HTML peuvent être ouverts dans un navigateur web pour une visualisation interactive.

