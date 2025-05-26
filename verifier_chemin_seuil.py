import pandas as pd
import networkx as nx

# === 1. Lire le dataset de pollution ===
df = pd.read_csv("qualite-de-lair-dans-le-reseau-de-transport-francilien.csv", sep=";")

# Nettoyer les noms de colonnes
df.columns = df.columns.str.strip()

# Garder uniquement les lignes de métro
df = df[df["Nom de la ligne"].str.contains("Métro", na=False)]

# === 2. Convertir les niveaux qualitatifs en scores numériques ===
niveau_map = {
    "pollution faible": 10,
    "pollution moyenne": 20,
    "pollution élevée": 30
}
df["pollution_num"] = df["niveau_pollution"].str.lower().map(niveau_map)

# Supprimer les lignes sans pollution reconnue
df = df.dropna(subset=["pollution_num", "Nom de la Station"])

# === 3. Créer le graphe avec pollution par station ===
G = nx.Graph()
for _, row in df.iterrows():
    station = row["Nom de la Station"]
    G.add_node(station, pollution=row["pollution_num"])

# === 4. Ajouter les connexions depuis graphe_metro.csv ===
connexions = pd.read_csv("graphe_metro.csv")
for _, row in connexions.iterrows():
    s1, s2 = row["station1"], row["station2"]
    if s1 in G.nodes and s2 in G.nodes:
        p1 = G.nodes[s1]["pollution"]
        p2 = G.nodes[s2]["pollution"]
        pollution_max = max(p1, p2)  # On prend la pire pollution entre les 2
        G.add_edge(s1, s2, pollution=pollution_max)

# === 5. Entrées utilisateur ===
station_depart = input("Station de départ : ").strip()
station_arrivee = input("Station d'arrivée : ").strip()

if station_depart not in G.nodes:
    print(f"❌ La station de départ '{station_depart}' n'existe pas dans le graphe.")
    exit()

if station_arrivee not in G.nodes:
    print(f"❌ La station d'arrivée '{station_arrivee}' n'existe pas dans le graphe.")
    exit()

try:
    seuil_pollution = float(input("Seuil de pollution maximum autorisé (ex: 15) : "))
except ValueError:
    print("⛔ Entrée invalide pour le seuil. Veuillez entrer un nombre.")
    exit()

# === 6. Filtrer les arêtes selon la pollution max autorisée ===
G_filtre = nx.Graph()
for u, v, data in G.edges(data=True):
    if data["pollution"] <= seuil_pollution:
        G_filtre.add_edge(u, v, pollution=data["pollution"])

# === 7. Résultat : vérifier l'existence d'un chemin filtré ===
if station_depart not in G_filtre.nodes or station_arrivee not in G_filtre.nodes:
    print("\n⛔ Une des stations n'est pas dans le graphe filtré (trop polluée ?).")
elif nx.has_path(G_filtre, station_depart, station_arrivee):
    chemin = nx.shortest_path(G_filtre, source=station_depart, target=station_arrivee)
    print("\n✅ Un chemin existe sous le seuil de pollution !")
    print(" → ".join(chemin))
else:
    print("\n❌ Aucun chemin possible respectant ce seuil de pollution.")

