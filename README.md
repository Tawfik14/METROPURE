
# 🌐 METROPURE - Analyse de la Pollution dans les Stations de Métro d'Île-de-France

Projet de data-science et de modélisation de graphe visant à analyser la pollution dans les stations du métro parisien.  
Il combine :

- Nettoyage de données (script R)
- Clustering (K-Means)
- Classification (K-NN enrichi)
- Modélisation & analyse de graphes (NetworkX)
- Analyse spectrale
- Visualisations
- Interface web interactive via Streamlit

---

## Sommaire

1. Prérequis
2. Installation
3. Lancer l’application
4. Scripts & fonctionnalités
5. Visualisations QGIS
6. Contact

---

## Prérequis

- **Python (3.10 minimum)**  
  ```bash
  # Créer puis activer un venv
  python -m venv venv
  source venv/bin/activate      # Linux/macOS
  venv\Scripts\activate.bat     # Windows

- **Paquets python**
  pandas
  numpy
  matplotlib
  seaborn
  scikit-learn
  networkx
  streamlit
  Pillow
  imbalanced-learn

- **R (4.0 minimum)** 

    Linux : sudo apt install r-base
    Windows : https://cran.r-project.org

---

## Installation

### 1. Récupérer le projet
```bash
 Clone le dépôt puis entre dans le dossier :
git clone https://github.com/<TON_GITHUB>/<TON_REPO>.git
cd <TON_REPO>

### 2. Installation paquets python
  ```bash
pip install -r requirements.txt


### 3. Installation paquets R
  ```bash
Rscript -e "install.packages(c('readr','dplyr','magrittr'), repos='https://cloud.r-project.org')"

### 4. Nettoyer le dataset
  Lance le script de nettoyage R :
  Rscript metro.R

---

## Lancer l'application
   ```bash
streamlit run app.py


Dans Streamlit :

  Téléverser le fichier CSV brut.
  Appuyer sur les boutons pour : Nettoyage → K-Means → K-NN → Graphe → Analyse spectrale....
  Observer / télécharger les graphes et PDF générés.

---

## Scripts & fonctionnalités

- **metro.R** : Nettoie le jeu de données ; supprime NA et doublons, filtre uniquement les stations de métro et génère un CSV propre.  
- **kmeans_pollution.py** : Applique un clustering K-Means (k = 3) sur latitude, longitude et score de pollution ; produit une carte des groupes.  
- **knn_pollution.py** : Pipeline complet StandardScaler → SMOTE → K-NN avec GridSearchCV ; affiche un rapport de classification et une matrice de confusion.  
- **generer_graphe_metro.py** : Parcourt les stations par ligne et crée la liste des connexions directes entre stations voisines (`graphe_metro.csv`).  
- **chemin_optimise.py** : Recherche le trajet à pollution minimale qui respecte un temps maximum saisi par l’utilisateur.  
- **verifier_chemin_seuil.py** : Vérifie l’existence d’un trajet dont la pollution ne dépasse pas un seuil donné.  
- **detecter_cycles.py** : Détecte et liste les cycles présents dans le réseau via `networkx.cycle_basis`.  
- **analyse_spectrale.py** : Calcule la matrice Laplacienne, les valeurs/vecteurs propres et trace l’énergie du signal de pollution dans le domaine spectral.  
- **visualiser_pollution_graphe.py** : Colore les nœuds du graphe selon un niveau de pollution simulé et génère une visualisation complète du réseau.  

---
 
## Visualisations QGIS

  Pollution_IDF.png : aperçu rapide
  Pollution_IDF.pdf : carte haute qualité

---

## Contact

Tawfik MOUHAMADIMAME : @Tawfik14
El Hadji DIONG       : @ElhadjiD
Mehdi LAHRACH        : @MehdiL
Ylang GUILLARD       : @ylangguillard
Albertine DUPUIS     : @albertineDupuis

Projet réalisés par des étudiants en ING 1 MF GM3
