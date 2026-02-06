"""
Script d'analyse pour le jeu de données des accidents corporels de la circulation.


Organisation du projet :
    data/accidents_insee.csv  : fichier CSV brut (extrait du ZIP de data.gouv.fr)
    outputs/                 : dossier où seront écrits les résultats et graphiques
    main.py                  : ce script

"""

import pandas as pd
import plotly.express as px
from pathlib import Path

# Définition des chemins de données et de sorties
# On calcule les chemins par rapport au répertoire contenant ce script afin de permettre
# l'exécution du script depuis n'importe quel endroit (le chemin relatif 'data/accidents_insee.csv'
# ne fonctionnerait pas si l'on se trouve dans un autre dossier).
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "accidents_insee.csv"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

def main() -> None:
    """Point d'entrée du script."""
    # Chargement des données avec pandas
    # Le fichier provient de data.gouv.fr et est encodé en ISO‑8859‑1 (latin1)
    print(f"Chargement du jeu de données depuis {DATA_FILE} …")
    df = pd.read_csv(DATA_FILE, sep=";", encoding="latin1")
    print(f"Jeu de données chargé. Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes")

    # Tentative de conversion des colonnes numériques en type numérique
    print("\nConversion des colonnes potentiellement numériques…")
    for col in df.columns:
        # On utilise errors='ignore' pour ne pas convertir les chaînes contenant des caractères non numériques
        try:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        except Exception:
            pass

    # Liste des colonnes numériques d'intérêt pour des statistiques rapides
    numeric_cols = [c for c in ['ttue', 'tbg', 'tbl', 'tindm', 'nbimplique'] if c in df.columns]
    if numeric_cols:
        print("\nStatistiques descriptives sur les colonnes numériques principales :")
        stats = df[numeric_cols].describe().transpose()
        print(stats)
    else:
        print("Aucune des colonnes attendues ('ttue', 'tbg', 'tbl', 'tindm', 'nbimplique') n'a été trouvée.")

    # 1. Graphique : Top des départements par nombre d'accidents (compte des lignes)
    if 'dep' in df.columns:
        print("\nGénération du graphique des départements les plus accidentogènes…")
        top_dep = df['dep'].value_counts().nlargest(15).reset_index()
        top_dep.columns = ['dep', 'count']
        fig1 = px.bar(
            top_dep,
            x='dep',
            y='count',
            title="Top 15 des départements par nombre d'accidents",
            labels={'dep': 'Département', 'count': 'Nombre d\'accidents'}
        )
        fig1.write_html(OUT_DIR / "01_top_dep_accidents.html")
    else:
        print("Colonne 'dep' introuvable : impossible de générer le top des départements.")

    # 2. Graphique : Distribution du nombre de tués par accident
    if 'ttue' in df.columns:
        print("Génération du graphique de distribution du nombre de tués par accident…")
        fig2 = px.histogram(
            df,
            x='ttue',
            nbins=50,
            title="Distribution du nombre de tués par accident",
            labels={'ttue': 'Nombre de tués'}
        )
        fig2.write_html(OUT_DIR / "02_distribution_ttue.html")
    else:
        print("Colonne 'ttue' introuvable : impossible de générer la distribution du nombre de tués.")

    # 3. Graphique : Répartition géographique (longitude vs latitude)
    if {'lat', 'long'}.issubset(df.columns):
        print("Génération du graphique de répartition géographique des accidents…")
        # Conversion explicite en nombre, remplaçant les valeurs non numériques par NaN
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['long'] = pd.to_numeric(df['long'], errors='coerce')
        fig3 = px.scatter(
            df.dropna(subset=['lat', 'long']),
            x='long',
            y='lat',
            title="Répartition géographique des accidents",
            labels={'long': 'Longitude', 'lat': 'Latitude'},
            opacity=0.3,
            height=600
        )
        fig3.write_html(OUT_DIR / "03_scatter_geo.html")
    else:
        print("Colonnes 'lat' et/ou 'long' introuvables : impossible de générer la carte des accidents.")

    # Sauvegarde du jeu de données nettoyé (avec conversions numériques)
    clean_csv_path = OUT_DIR / "clean_accidents_insee.csv"
    df.to_csv(clean_csv_path, index=False)
    print(f"\nFichier nettoyé enregistré : {clean_csv_path}")
    print("Tous les graphiques ont été générés dans le dossier 'outputs'.")

if __name__ == '__main__':
    main()