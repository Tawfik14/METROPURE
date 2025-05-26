import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import scipy.linalg as la
import unicodedata

# Fonction de nettoyage
def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")  # Enlève les accents
    return text.strip()

# On va charger les données
df_graph = pd.read_csv("graphe_metro.csv")
df_pollution = pd.read_csv("qualite-de-lair-dans-le-reseau-de-transport-francilien.csv", sep=";")

# Nettoyage
df_pollution.columns = [col.strip().lower() for col in df_pollution.columns]
df_pollution["nom de la ligne"] = df_pollution["nom de la ligne"].str.lower()

# Filtrage métro uniquement
df_metro = df_pollution[df_pollution["nom de la ligne"].str.contains("métro", na=False)].copy()

# On va faire le Mapping
pollution_map = {
    "pollution faible": 1,
    "pollution moyenne": 3,
    "pollution élevée": 5
}
df_metro["niveau_pollution"] = df_metro["niveau_pollution"].str.lower()
df_metro = df_metro[df_metro["niveau_pollution"].isin(pollution_map)].copy()
df_metro["pollution_num"] = df_metro["niveau_pollution"].map(pollution_map)
df_metro["station_norm"] = df_metro["nom de la station"].apply(normalize)

# Moyenne pollution par station
pollution_par_station = df_metro.groupby("station_norm")["pollution_num"].mean().to_dict()

# On va construire le graphe
G = nx.Graph()
for _, row in df_graph.iterrows():
    s1 = normalize(row["station1"])
    s2 = normalize(row["station2"])
    G.add_edge(s1, s2, weight=1)


stations = list(G.nodes())
pollution_signal = [pollution_par_station.get(station, np.nan) for station in stations]
valid_indices = [i for i, val in enumerate(pollution_signal) if not np.isnan(val)]
stations_valid = [stations[i] for i in valid_indices]
pollution_signal_valid = np.array([pollution_signal[i] for i in valid_indices])
G_sub = G.subgraph(stations_valid).copy()

# On aura l'analyse spectrale
if G_sub.number_of_nodes() > 0 and G_sub.number_of_edges() > 0:
    print(" Sous-graphe avec pollution valide :")
    print(f" - {G_sub.number_of_nodes()} stations")
    print(f" - {G_sub.number_of_edges()} connexions\n")

    L = nx.laplacian_matrix(G_sub).todense()
    eigvals, eigvecs = la.eigh(L)

    # Affichage des valeurs propres principales
    print("Top 10 valeurs propres de la matrice de Laplace :")
    print(np.round(eigvals[:10], 4))
    print()

    # Projection spectrale
    spectral_signal = eigvecs.T @ pollution_signal_valid

    # Affichage
    plt.figure(figsize=(10, 4))
    plt.plot(spectral_signal**2, marker='o')
    plt.title("Énergie du signal de pollution dans le domaine spectral (réel)")
    plt.xlabel("Indice du vecteur propre")
    plt.ylabel("Énergie (amplitude²)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("spectre_pollution.png", dpi=300)

    print("Analyse spectrale terminée. Fichier généré : spectre_pollution.png")
else:
    print("Erreur : le graphe avec pollution valide est vide.")

