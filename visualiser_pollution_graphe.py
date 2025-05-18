import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Charger les connexions
df = pd.read_csv("graphe_metro.csv")

# Générer une pollution aléatoire pour chaque station
stations = pd.concat([df["station1"], df["station2"]]).unique()
pollution_station = {station: np.random.uniform(1, 5) for station in stations}

# Créer le graphe
G = nx.Graph()
for _, row in df.iterrows():
    s1, s2 = row["station1"], row["station2"]
    G.add_edge(s1, s2)

# Attribuer la pollution comme attribut de nœud
nx.set_node_attributes(G, pollution_station, name="pollution")

# Préparer les couleurs des nœuds
node_colors = [G.nodes[n]["pollution"] for n in G.nodes()]

# Générer une disposition des nœuds (graphe spatial)
pos = nx.spring_layout(G, seed=42)  # stable layout

# Dessiner le graphe avec colorbar fonctionnelle
plt.figure(figsize=(15, 12))

# Arêtes
nx.draw_networkx_edges(G, pos, alpha=0.3)

# Nœuds colorés par pollution
nodes = nx.draw_networkx_nodes(
    G,
    pos,
    node_color=node_colors,
    cmap=plt.cm.plasma,
    node_size=100
)

# Labels
nx.draw_networkx_labels(G, pos, font_size=6)

# Barre de couleur liée au "mappable" nodes
plt.colorbar(nodes, label="Niveau de pollution")

plt.title("Visualisation de la pollution par station sur le graphe métro")
plt.axis("off")
plt.tight_layout()
plt.show()

