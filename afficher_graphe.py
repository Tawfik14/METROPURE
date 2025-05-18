import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Lire les connexions
df = pd.read_csv("graphe_metro.csv")

# Créer un graphe non orienté
G = nx.Graph()

# Ajouter les arêtes à partir du CSV
for _, row in df.iterrows():
    G.add_edge(row["station1"], row["station2"])

# Dessiner le graphe (petit affichage simple)
plt.figure(figsize=(12, 10))
nx.draw(G, with_labels=True, node_size=50, font_size=8)
plt.title("Graphe des stations de métro")
plt.tight_layout()
plt.show()

