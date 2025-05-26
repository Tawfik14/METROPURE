import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import unicodedata

# Fonction pour normaliser les noms de station
def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")  # supprime les accents
    return text.strip()

# Charger les fichiers
df_graph = pd.read_csv("graphe_metro.csv")
df_pollution = pd.read_csv("qualite-de-lair-dans-le-reseau-de-transport-francilien.csv", sep=";")

# Nettoyer les colonnes et filtrer les stations de métro
df_pollution.columns = [col.strip().lower() for col in df_pollution.columns]
df_pollution["nom de la ligne"] = df_pollution["nom de la ligne"].str.lower()
df_metro = df_pollution[df_pollution["nom de la ligne"].str.contains("métro", na=False)].copy()

# Ici on va mapper
pollution_map = {
    "pollution faible": 1,
    "pollution moyenne": 3,
    "pollution élevée": 5
}
df_metro["niveau_pollution"] = df_metro["niveau_pollution"].str.lower()
df_metro = df_metro[df_metro["niveau_pollution"].isin(pollution_map)].copy()
df_metro["pollution_num"] = df_metro["niveau_pollution"].map(pollution_map)
df_metro["station_norm"] = df_metro["nom de la station"].apply(normalize)


pollution_par_station = df_metro.groupby("station_norm")["pollution_num"].mean().to_dict()


G = nx.Graph()
for _, row in df_graph.iterrows():
    s1 = normalize(row["station1"])
    s2 = normalize(row["station2"])
    G.add_edge(s1, s2)


stations = list(G.nodes())
pollution_station = {station: pollution_par_station.get(station, 0) for station in stations}
nx.set_node_attributes(G, pollution_station, name="pollution")


node_colors = [G.nodes[n]["pollution"] for n in G.nodes()]


pos = nx.spring_layout(G, seed=42)


plt.figure(figsize=(15, 12))
nx.draw_networkx_edges(G, pos, alpha=0.3)
nodes = nx.draw_networkx_nodes(
    G,
    pos,
    node_color=node_colors,
    cmap=plt.cm.plasma,
    node_size=100
)
nx.draw_networkx_labels(G, pos, font_size=6)
plt.colorbar(nodes, label="Niveau de pollution (1 = faible, 5 = élevé)")
plt.title("Visualisation réelle de la pollution par station (métro)")
plt.axis("off")
plt.tight_layout()
plt.savefig("pollution_graphe.png", dpi=300)
print(" Visualisation enregistrée : pollution_graphe.png")

