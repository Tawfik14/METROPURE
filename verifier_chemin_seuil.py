import pandas as pd
import networkx as nx
import random

# Charger les connexions depuis le fichier
df = pd.read_csv("graphe_metro.csv")

# Simuler la pollution par segment (si pas déjà faite)
df["pollution"] = df.apply(lambda _: random.uniform(1, 5), axis=1)

# Construire le graphe avec poids pollution
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["station1"], row["station2"], pollution=row["pollution"])

# Saisie utilisateur
station_depart = input("Station de départ : ")
station_arrivee = input("Station d'arrivée : ")
seuil_pollution = float(input("Seuil de pollution maximum autorisé (ex: 3.5) : "))

# Créer une copie du graphe contenant uniquement les segments sous le seuil
G_filtre = nx.Graph()
for u, v, data in G.edges(data=True):
    if data["pollution"] <= seuil_pollution:
        G_filtre.add_edge(u, v, pollution=data["pollution"])

# Vérification de l'existence d’un chemin
if nx.has_path(G_filtre, station_depart, station_arrivee):
    chemin = nx.shortest_path(G_filtre, source=station_depart, target=station_arrivee)
    print("\n✅ Un chemin existe sous le seuil de pollution !")
    print(" → ".join(chemin))
else:
    print("\n❌ Aucun chemin possible respectant ce seuil.")

