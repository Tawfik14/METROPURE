import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Charger le fichier CSV nettoyé
df = pd.read_csv("stations_metro_propre.csv")

# Garder les colonnes utiles
df_clean = df[["Nom de la Station", "stop_lat", "stop_lon", "niveau_pollution"]].copy()

# Garder uniquement les lignes avec pollution exploitable
niveaux_valides = ["pollution faible", "pollution moyenne", "pollution élevée"]
df_clean = df_clean[df_clean["niveau_pollution"].isin(niveaux_valides)]

# Encodage : convertir texte en score numérique
encodage = {
    "pollution faible": 1,
    "pollution moyenne": 2,
    "pollution élevée": 3
}
df_clean["pollution_score"] = df_clean["niveau_pollution"].map(encodage)

# Supprimer les lignes avec données manquantes
df_clean = df_clean.dropna(subset=["stop_lat", "stop_lon", "pollution_score"])

# Mise à l’échelle des coordonnées + pollution
features = df_clean[["stop_lat", "stop_lon", "pollution_score"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# Appliquer K-means (choisir 3 clusters)
kmeans = KMeans(n_clusters=3, random_state=42)
df_clean["cluster"] = kmeans.fit_predict(X_scaled)

# Visualisation
plt.figure(figsize=(10, 6))
plt.scatter(df_clean["stop_lon"], df_clean["stop_lat"], c=df_clean["cluster"], cmap="Set1", s=50)
plt.title("Clustering des stations métro selon pollution et géographie (K-means)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.tight_layout()
plt.show()

