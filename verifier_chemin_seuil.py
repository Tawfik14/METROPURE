
import pandas as pd
import networkx as nx

# Lire le dataset réel
df = pd.read_csv("qualite-de-lair-dans-le-reseau-de-transport-francilien.csv", sep=";")

# Garder uniquement les lignes de métro
df = df[df["Nom de la ligne"].str.contains("Métro", na=False)]

# Mapper les niveaux de pollution
niveau_map = {
    "pollution faible": 10,
    "pollution moyenne": 20,
    "pollution forte": 30
}
df["pollution_num"] = df["niveau_pollution"].map(niveau_map)

# Supprimer les lignes sans pollution connue
df = df.dropna(subset=["pollution_num"])

# Créer un graphe avec les stations comme nœuds
G = nx.Graph()
for _, row in df.iterrows():
    station = row["Nom de la Station"]
    G.add_node(station, pollution=row["pollution_num"])

# Lire les connexions entre stations
connexions = pd.read_csv("graphe_metro.csv")
for _, row in connexions.iterrows():
    s1, s2 = row["station1"], row["station2"]
    if s1 in G.nodes and s2 in G.nodes:
        p1 = G.nodes[s1]["pollution"]
        p2 = G.nodes[s2]["pollution"]
        pollution_max = max(p1, p2)  # On prend la pollution la plus élevée
        G.add_edge(s1, s2, pollution=pollution_max)

# Entrée utilisateur avec validation
station_depart = input("Station de départ : ").strip()
station_arrivee = input("Station d'arrivée : ").strip()

if station_depart not in G.nodes:
    print(f"❌ La station de départ '{station_depart}' n'existe pas.")
    exit()

if station_arrivee not in G.nodes:
    print(f"❌ La station d'arrivée '{station_arrivee}' n'existe pas.")
    exit()

try:
    seuil_pollution = float(input("Seuil de pollution maximum autorisé (ex: 20) : "))
except ValueError:
    print("❌ Entrée invalide pour le seuil de pollution. Veuillez entrer un nombre.")
    exit()

# Filtrer le graphe
G_filtre = nx.Graph()
for u, v, data in G.edges(data=True):
    if data["pollution"] <= seuil_pollution:
        G_filtre.add_edge(u, v, pollution=data["pollution"])

# Résultat
if station_depart not in G_filtre.nodes or station_arrivee not in G_filtre.nodes:
    print("\n❌ Une des stations n'est pas dans le graphe filtré (trop polluée ?).")
elif nx.has_path(G_filtre, station_depart, station_arrivee):
    chemin = nx.shortest_path(G_filtre, source=station_depart, target=station_arrivee)
    print("\n✅ Un chemin existe sous le seuil de pollution !")
    print(" → ".join(chemin))
else:
    print("\n❌ Aucun chemin possible respectant ce seuil.")
