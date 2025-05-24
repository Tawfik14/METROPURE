import pandas as pd
import networkx as nx
import random


df = pd.read_csv("graphe_metro.csv")


df["pollution"] = df.apply(lambda _: random.uniform(1, 5), axis=1)
df["temps"] = 2  


G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["station1"], row["station2"], pollution=row["pollution"], temps=row["temps"])


station_depart = input("Station de départ : ")
station_arrivee = input("Station d'arrivée : ")
temps_max = float(input("Temps de trajet maximum (en minutes) : "))


all_paths = list(nx.all_simple_paths(G, source=station_depart, target=station_arrivee, cutoff=20))


chemin_optimal = None
pollution_min = float('inf')

for path in all_paths:
    total_temps = sum(G[u][v]['temps'] for u, v in zip(path[:-1], path[1:]))
    total_pollution = sum(G[u][v]['pollution'] for u, v in zip(path[:-1], path[1:]))

    if total_temps <= temps_max and total_pollution < pollution_min:
        pollution_min = total_pollution
        chemin_optimal = path


if chemin_optimal:
    print("\n✅ Chemin optimal trouvé :")
    print(" → ".join(chemin_optimal))
    print(f"Temps total : {total_temps:.1f} min")
    print(f"Pollution totale : {pollution_min:.2f}")
else:
    print("\n❌ Aucun chemin trouvé respectant la contrainte de temps.")

