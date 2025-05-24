import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("graphe_metro.csv")


stations = pd.concat([df["station1"], df["station2"]]).unique()
pollution_station = {station: np.random.uniform(1, 5) for station in stations}


G = nx.Graph()
for _, row in df.iterrows():
    s1, s2 = row["station1"], row["station2"]
    G.add_edge(s1, s2)


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


plt.colorbar(nodes, label="Niveau de pollution")

plt.title("Visualisation de la pollution par station sur le graphe métro")
plt.axis("off")
plt.tight_layout()
plt.savefig("pollution_graphe.png", dpi=300)


