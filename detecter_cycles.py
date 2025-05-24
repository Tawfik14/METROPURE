import pandas as pd
import networkx as nx


df = pd.read_csv("graphe_metro.csv")


G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["station1"], row["station2"])


try:
    cycles = list(nx.cycle_basis(G))  
    if cycles:
        print(f"\n✅ Cycles détectés : {len(cycles)}")
        for i, cycle in enumerate(cycles[:5]):
            print(f"Cycle {i+1} : {' → '.join(cycle)}")
    else:
        print("\n❌ Aucun cycle détecté dans le graphe.")
except Exception as e:
    print("Erreur :", e)

