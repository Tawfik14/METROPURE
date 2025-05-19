import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# Charger le fichier
df = pd.read_csv("stations_metro_propre.csv")

# Garder uniquement les stations avec pollution exploitable
niveaux_valides = ["pollution faible", "pollution moyenne", "pollution élevée"]
df = df[df["niveau_pollution"].isin(niveaux_valides)]

# Encodage pollution
encodage = {
    "pollution faible": 0,
    "pollution moyenne": 1,
    "pollution élevée": 2
}
df["pollution_label"] = df["niveau_pollution"].map(encodage)

# Supprimer les lignes incomplètes
df = df.dropna(subset=["stop_lat", "stop_lon", "pollution_label"])

# Séparer X (features) et y (cible)
X = df[["stop_lat", "stop_lon"]]
y = df["pollution_label"]

# Standardisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Créer le modèle k-NN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Prédiction
y_pred = knn.predict(X_test)

# Évaluation
print("✅ Rapport de classification :")
print(classification_report(y_test, y_pred, target_names=["faible", "moyenne", "élevée"]))

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred)
print("Matrice de confusion :")
print(cm)

