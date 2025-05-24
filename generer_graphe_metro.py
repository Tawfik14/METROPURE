import pandas as pd


nom_fichier = "qualite-de-lair-dans-le-reseau-de-transport-francilien.csv"


df = pd.read_csv(nom_fichier, sep=';')


metro_df = df[df["Nom de la ligne"].str.contains("Métro", case=False, na=False)]


metro_df_sorted = metro_df.sort_values(by=["Nom de la ligne", "stop_lat"])


connections = []

for ligne, group in metro_df_sorted.groupby("Nom de la ligne"):
    stations = group["Nom de la Station"].tolist()
    for i in range(len(stations) - 1):
        connections.append({
            "station1": stations[i],
            "station2": stations[i + 1],
            "trajet_existe": True
        })


graphe_df = pd.DataFrame(connections)


nom_fichier_sortie = "graphe_metro.csv"
graphe_df.to_csv(nom_fichier_sortie, index=False)

print(f"Le fichier '{nom_fichier_sortie}' a été créé avec {len(graphe_df)} connexions.")

