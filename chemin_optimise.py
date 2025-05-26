import pandas as pd
import networkx as nx

# === 1. Charger les connexions entre stations ===
df_graph = pd.read_csv("graphe_metro.csv")

# === 2. Charger les vraies données de pollution qualitative ===
df_pollution = pd.read_csv("qualite-de-lair-dans-le-reseau-de-transport-francilien.csv", sep=';')

# Nettoyer les noms de colonnes
df_pollution.columns = df_pollution.columns.str.strip()

# Garder uniquement les stations avec info pollution
df_pollution = df_pollution.dropna(subset=["Nom de la Station", "niveau_pollution"])

# Filtrer uniquement les stations souterraines (supprimer "station aérienne", "pas de données")
df_pollution = df_pollution[~df_pollution["niveau_pollution"].str.contains("station aérienne|pas de données", case=False, na=False)]

# === 3. Convertir pollution textuelle → score numérique ===
pollution_map = {
    "pollution faible": 1,
    "pollution moyenne": 3,
    "pollution élevée": 5
}
df_pollution["pollution"] = df_pollution["niveau_pollution"].str.lower().map(pollution_map)

# Supprimer les lignes non converties (ex : NaN, inconnues)
df_pollution = df_pollution.dropna(subset=["pollution"])

# === 4. Calcul de la pollution moyenne par station ===
pollution_station = df_pollution.groupby("Nom de la Station")["pollution"].mean().reset_index()
pollution_station.columns = ["station", "pollution"]

# === 5. Ajouter pollution moyenne au graphe ===
# Merge avec station1
df_graph = df_graph.merge(pollution_station, left_on="station1", right_on="station", how="left")
df_graph = df_graph.rename(columns={"pollution": "poll1"}).drop(columns=["station"])

# Merge avec station2
df_graph = df_graph.merge(pollution_station, left_on="station2", right_on="station", how="left")
df_graph = df_graph.rename(columns={"pollution": "poll2"}).drop(columns=["station"])

# Calcul de la pollution moyenne entre les deux stations
df_graph["pollution"] = (df_graph["poll1"] + df_graph["poll2"]) / 2
df_graph["temps"] = 2

df_graph = df_graph.drop(columns=["poll1", "poll2"])

# === 6. Construire le graphe pondéré ===
G = nx.Graph()
for _, row in df_graph.iterrows():
    if pd.notna(row["pollution"]):
        G.add_edge(row["station1"], row["station2"],
                   pollution=row["pollution"], temps=row["temps"])

# === 7. Demander les entrées utilisateur ===
station_depart = input("Station de départ : ")
station_arrivee = input("Station d'arrivée : ")
temps_max = float(input("Temps de trajet maximum (en minutes) : "))

# === 8. Recherche des chemins valides (max 20 étapes) ===
try:
    all_paths = list(nx.all_simple_paths(G, source=station_depart, target=station_arrivee, cutoff=20))
except nx.NetworkXNoPath:
    print("❌ Aucun chemin trouvé entre ces deux stations.")
    exit()

# === 9. Sélection du chemin optimal (pollution minimale, temps ≤ max) ===
chemin_optimal = None
pollution_min = float('inf')

for path in all_paths:
    total_temps = sum(G[u][v]['temps'] for u, v in zip(path[:-1], path[1:]))
    total_pollution = sum(G[u][v]['pollution'] for u, v in zip(path[:-1], path[1:]))

    if total_temps <= temps_max and total_pollution < pollution_min:
        pollution_min = total_pollution
        chemin_optimal = path

# === 10. Affichage du résultat ===
if chemin_optimal:
    print("\n✅ Chemin optimal trouvé :")
    print(" → ".join(chemin_optimal))
    print(f"🕒 Temps total : {total_temps:.1f} min")
    print(f"🌫️ Pollution totale (score) : {pollution_min:.2f}")
else:
    print("\n❌ Aucun chemin trouvé respectant la contrainte de temps.")

