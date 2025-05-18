import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la

# 1. Charger les connexions et ajouter un signal de pollution aléatoire
df = pd.read_csv("graphe_metro.csv")
df["pollution"] = df.apply(lambda _: np.random.uniform(1, 5), axis=1)  # pollution simulée

# 2. Construire le graphe
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row["station1"], row["station2"], weight=1, pollution=row["pollution"])

# 3. Calcul de la matrice de Laplace
L = nx.laplacian_matrix(G).todense()

print("✅ Matrice de Laplace générée avec succès !")
print(f"Taille : {L.shape}")

# 4. Décomposition spectrale (valeurs et vecteurs propres)
eigvals, eigvecs = la.eigh(L)  # Matrice symétrique → eigh
print(f"\nTop 10 valeurs propres de L :\n{eigvals[:10]}")

# 5. Générer un signal de pollution station par station
stations = list(G.nodes())
pollution_signal = np.random.uniform(1, 5, size=len(stations))

# 6. Projeter le signal dans la base spectrale
spectral_signal = eigvecs.T @ pollution_signal

# 7. Visualiser l'énergie du signal dans le domaine spectral
plt.figure(figsize=(10, 4))
plt.plot(spectral_signal**2, marker='o')
plt.title("Énergie du signal de pollution dans le domaine spectral")
plt.xlabel("Indice du vecteur propre")
plt.ylabel("Énergie (amplitude²)")
plt.grid(True)
plt.tight_layout()
plt.show()

