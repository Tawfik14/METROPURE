import streamlit as st
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
from PIL import Image
import os

st.set_page_config(page_title="Analyse Pollution - Métro IDF", layout="wide")
st.title("Analyse de la pollution dans les stations de métro d'Île-de-France")

#  Chargement des données du fichier
uploaded_file = st.file_uploader(
    "Uploader le fichier CSV brut (avec point-virgule comme séparateur)",
    type=["csv"],
)

if uploaded_file:
    with open(
        "qualite-de-lair-dans-le-reseau-de-transport-francilien.csv", "wb"
    ) as f:
        f.write(uploaded_file.read())
    st.success(
        "Fichier sauvegardé sous "
        "'qualite-de-lair-dans-le-reseau-de-transport-francilien.csv'"
    )

    #  Nettoyage et filtrage avec le script R 
    st.subheader("Nettoyage et filtrage (script R)")
    if st.button("Lancer le script R (metro.R)"):
        result = subprocess.run(["Rscript", "metro.R"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("Script R exécuté avec succès.")
            st.code(result.stdout, language="text")
        else:
            st.error("Erreur dans le script R :")
            st.text(result.stderr)

    #  Clustering kmeans
    st.subheader("Clustering KMeans (script Python)")
    if st.button("Lancer le clustering KMeans"):
        result = subprocess.run(
            ["python3", "kmeans_pollution.py"], capture_output=True, text=True
        )
        if result.returncode == 0:
            st.success("Clustering KMeans effectué avec succès.")
            if os.path.exists("graph_kmeans.png"):
                st.image(
                    Image.open("graph_kmeans.png"),
                    caption="Clusters de pollution (KMeans)",
                    use_column_width=True,
                )
            else:
                st.warning("Le fichier 'graph_kmeans.png' n'a pas été trouvé.")
        else:
            st.error("Erreur dans le script Python :")
            st.text(result.stderr)

    # Pour la classification knn
    st.subheader("Classification KNN (script Python)")
    if st.button("Lancer la classification KNN"):
        result = subprocess.run(
            ["python3", "knn_pollution.py"], capture_output=True, text=True
        )
        if result.returncode == 0:
            st.success("Classification KNN effectuée avec succès.")
            st.code(result.stdout, language="text")
            if os.path.exists("graph_knn_confusion.png"):
                st.image(
                    Image.open("graph_knn_confusion.png"),
                    caption="Matrice de confusion (KNN)",
                    use_column_width=True,
                )
            else:
                st.warning("Le fichier 'graph_knn_confusion.png' n'a pas été trouvé.")
        else:
            st.error("Erreur dans le script Python :")
            st.text(result.stderr)

    #  Carte QGIS 
    st.subheader("Carte QGIS – Visualisation géographique de la pollution")

    if os.path.exists("Pollution_IDF.png"):
        st.image(
            Image.open("Pollution_IDF.png"),
            caption="Carte des niveaux de pollution – QGIS (PNG)",
            use_column_width=True,
        )
    else:
        st.warning("Le fichier 'Pollution_IDF.png' n'a pas été trouvé.")

    if os.path.exists("Pollution_IDF.pdf"):
        with open("Pollution_IDF.pdf", "rb") as pdf_file:
            st.download_button(
                label="📥 Télécharger la carte QGIS (PDF haute qualité)",
                data=pdf_file,
                file_name="Pollution_IDF.pdf",
                mime="application/pdf",
            )
    else:
        st.warning("Le fichier 'Pollution_IDF.pdf' n'a pas été trouvé.")

    # Pour générer le graphe métro 
    st.subheader("Graphe des connexions entre stations (Partie 2)")
    if st.button("Générer le fichier de graphe métro"):
        result = subprocess.run(
            ["python3", "generer_graphe_metro.py"], capture_output=True, text=True
        )
        if result.returncode == 0:
            st.success("Fichier de graphe généré avec succès.")
            st.code(result.stdout, language="text")
        else:
            st.error("Erreur lors de la génération du graphe :")
            st.text(result.stderr)

    # Chemin optimal, pollution et temps 
    st.subheader("Chemin optimal (pollution minimale sous contrainte de temps)")
    station_depart = st.text_input("Station de départ")
    station_arrivee = st.text_input("Station d'arrivée")
    temps_max = st.number_input(
        "Temps maximum autorisé (minutes)", min_value=1.0, step=1.0
    )

    if st.button("Calculer le chemin optimal"):
        chemin_input = f"{station_depart}\n{station_arrivee}\n{temps_max}\n"
        result = subprocess.run(
            ["python3", "chemin_optimise.py"],
            input=chemin_input,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            st.success("Chemin calculé avec succès.")
            st.code(result.stdout, language="text")
        else:
            st.error("Erreur lors du calcul du chemin :")
            st.text(result.stderr)

    #  Chemin sous un seuil de pollution 
    st.subheader("Chemin respectant un seuil de pollution maximal")
    station_depart_seuil = st.text_input(
        "Station de départ (seuil)", key="dep_seuil"
    )
    station_arrivee_seuil = st.text_input(
        "Station d'arrivée (seuil)", key="arr_seuil"
    )
    seuil_pollution = st.number_input(
        "Seuil de pollution maximum autorisé", min_value=0.0, step=1.0
    )

    if st.button("Vérifier un chemin sous le seuil de pollution"):
        saisie = (
            f"{station_depart_seuil}\n"
            f"{station_arrivee_seuil}\n"
            f"{seuil_pollution}\n"
        )
        result = subprocess.run(
            ["python3", "verifier_chemin_seuil.py"],
            input=saisie,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            st.success("Résultat du test de chemin :")
            st.code(result.stdout, language="text")
        else:
            st.error("Erreur lors de l'exécution du script :")
            st.text(result.stderr)

    #  Détection de cycles 
    st.subheader("Détection de cycles dans le graphe des stations")
    if st.button("Détecter les cycles"):
        result = subprocess.run(
            ["python3", "detecter_cycles.py"], capture_output=True, text=True
        )
        if result.returncode == 0:
            st.success("Résultat de la détection :")
            st.code(result.stdout, language="text")
        else:
            st.error("Erreur lors de la détection des cycles :")
            st.text(result.stderr)

    #  L'analyse spectrale  
    st.subheader("Analyse spectrale de la pollution sur le graphe (Partie 3)")
    if st.button("Lancer l'analyse spectrale"):
        result = subprocess.run(
            ["python3", "analyse_spectrale.py"], capture_output=True, text=True
        )
        if result.returncode == 0:
            st.success("Analyse spectrale terminée.")
            st.code(result.stdout, language="text")
            if os.path.exists("spectre_pollution.png"):
                st.image(
                    Image.open("spectre_pollution.png"),
                    caption="Énergie du signal de pollution – Domaine spectral",
                    use_column_width=True,
                )
            else:
                st.warning("L'illustration 'spectre_pollution.png' n'a pas été trouvée.")
        else:
            st.error("Erreur lors de l'analyse spectrale :")
            st.text(result.stderr)

    #  Pollution par station sur le graphe 
    st.subheader("Pollution par station sur le graphe")
    if st.button("Afficher pollution sur graphe"):
        result = subprocess.run(
            ["python3", "visualiser_pollution_graphe.py"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            st.success("Visualisation générée.")
            st.code(result.stdout, language="text")
            if os.path.exists("pollution_graphe.png"):
                st.image(
                    Image.open("pollution_graphe.png"),
                    caption="Pollution par station (couleur/épaisseur)",
                    use_column_width=True,
                )
            else:
                st.warning(
                    "Le fichier 'pollution_graphe.png' n'a pas été trouvé. "
                    "Assure-toi que ton script appelle "
                    "plt.savefig('pollution_graphe.png', dpi=300)."
                )
        else:
            st.error("Erreur lors de la visualisation :")
            st.text(result.stderr)

    #  Affichage du graphe 
    if st.button("Afficher le graphe des stations"):
        result = subprocess.run(
            ["python3", "afficher_graphe.py"], capture_output=True, text=True
        )
        if result.returncode == 0:
            st.success("Graphe affiché avec succès.")
            if os.path.exists("graphe.png"):
                st.image(
                    Image.open("graphe.png"),
                    caption="Graphe des stations de métro",
                    use_column_width=True,
                )
            else:
                st.warning("Le fichier 'graphe.png' n'a pas été trouvé.")
        else:
            st.error("Erreur lors de l'affichage du graphe :")
            st.text(result.stderr)

else:
    st.info("Veuillez uploader un fichier pour commencer.")

