import pandas as pd

# 1. Charger le fichier CSV d'origine (assure-toi que le fichier est dans le même dossier)
nom_fichier = "qualite-de-lair-dans-le-reseau-de-transport-francilien.csv"

# Lire avec le bon séparateur (point-virgule)
df = pd.read_csv(nom_fichier, sep=';')

# 2. Garder uniquement les stations de métro
metro_df = df[df["Nom de la ligne"].str.contains("Métro", case=False, na=False)]

# 3. Trier les stations par ligne puis par latitude (approximation de l’ordre des stations)
metro_df_sorted = metro_df.sort_values(by=["Nom de la ligne", "stop_lat"])

# 4. Construire les connexions simulées entre stations voisines sur chaque ligne
connections = []

for ligne, group in metro_df_sorted.groupby("Nom de la ligne"):
    stations = group["Nom de la Station"].tolist()
    for i in range(len(stations) - 1):
        connections.append({
            "station1": stations[i],
            "station2": stations[i + 1],
            "trajet_existe": True
        })

# 5. Créer un DataFrame à partir des connexions
graphe_df = pd.DataFrame(connections)

# 6. Sauvegarder en CSV
nom_fichier_sortie = "graphe_metro.csv"
graphe_df.to_csv(nom_fichier_sortie, index=False)

print(f"Le fichier '{nom_fichier_sortie}' a été créé avec {len(graphe_df)} connexions.")

