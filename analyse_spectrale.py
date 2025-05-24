import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la


df = pd.read_csv("graphe_metro.csv")
df["pollution"] = df.apply(lambda _: np.random.uniform(1, 5), axis=1)  


G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["station1"], row["station2"], weight=1, pollution=row["pollution"])


L = nx.laplacian_matrix(G).todense()

print("✅ Matrice de Laplace générée avec succès !")
print(f"Taille : {L.shape}")


eigvals, eigvecs = la.eigh(L)  
print(f"\nTop 10 valeurs propres de L :\n{eigvals[:10]}")


stations = list(G.nodes())
pollution_signal = np.random.uniform(1, 5, size=len(stations))


spectral_signal = eigvecs.T @ pollution_signal


plt.figure(figsize=(10, 4))
plt.plot(spectral_signal**2, marker='o')
plt.title("Énergie du signal de pollution dans le domaine spectral")
plt.xlabel("Indice du vecteur propre")
plt.ylabel("Énergie (amplitude²)")
plt.grid(True)
plt.tight_layout()
plt.savefig("spectre_pollution.png", dpi=300)


