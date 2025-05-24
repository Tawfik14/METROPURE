import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import itertools
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# ------------------------------------------------------------------
# 1. Lecture et préparation des données
# ------------------------------------------------------------------
df = pd.read_csv("stations_metro_propre.csv")

df_clean = df[["Nom de la Station", "stop_lat", "stop_lon", "niveau_pollution"]].copy()
niveaux_valides = ["pollution faible", "pollution moyenne", "pollution élevée"]
df_clean = df_clean[df_clean["niveau_pollution"].isin(niveaux_valides)]

encodage = {"pollution faible": 1, "pollution moyenne": 2, "pollution élevée": 3}
df_clean["pollution_score"] = df_clean["niveau_pollution"].map(encodage)

df_clean = df_clean.dropna(subset=["stop_lat", "stop_lon", "pollution_score"])


# ------------------------------------------------------------------
# 2. K-means → groupes
# ------------------------------------------------------------------
features = df_clean[["stop_lat", "stop_lon", "pollution_score"]]
X_scaled = StandardScaler().fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42)
df_clean["groupe"] = kmeans.fit_predict(X_scaled)


# ------------------------------------------------------------------
# 3. Visualisation
# ------------------------------------------------------------------
plt.figure(figsize=(10, 6))

# --- palette pollution (bleu → violet → rose) ---
couleurs_pollution = {
    "pollution faible":  "#4A90E2",   # bleu
    "pollution moyenne": "#8B5CF6",   # violet
    "pollution élevée":  "#D11A8B"    # magenta-rose
}

# --- formes pour les groupes ---
marker_cycle = itertools.cycle(["o", "s", "P", "D", "^", "v", "<", ">", "X"])
marker_par_groupe = {}   # on mémorise la forme attribuée à chaque groupe

for gid in sorted(df_clean["groupe"].unique()):
    subset = df_clean[df_clean["groupe"] == gid]
    mk = next(marker_cycle)
    marker_par_groupe[gid] = mk                      # on retient la forme
    couleurs_points = subset["niveau_pollution"].map(couleurs_pollution)
    plt.scatter(
        subset["stop_lon"], subset["stop_lat"],
        c=couleurs_points,
        marker=mk,
        s=60,
        edgecolor="k",
        linewidth=0.5
    )

# ---------- 2 légendes ----------
ax = plt.gca()

# 1) Légende groupes (formes, fond blanc)
handles_groupes = [
    Line2D([0], [0], marker=marker_par_groupe[gid],
           markerfacecolor="white", markeredgecolor="k",
           markersize=8, linestyle="None", label=f"Groupe {gid}")
    for gid in sorted(marker_par_groupe)
]
leg_groupes = ax.legend(handles=handles_groupes, title="Groupes", loc="upper right")
ax.add_artist(leg_groupes)

# 2) Légende pollution (couleurs)
handles_pollution = [
    mpatches.Patch(color=col, label=lib.replace("pollution ", "").capitalize())
    for lib, col in couleurs_pollution.items()
]
plt.legend(handles=handles_pollution, title="Niveau pollution", loc="lower left")
# ---------------------------------

plt.title("Stations de métro : groupes & niveau de pollution")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig("graph_kmeans.png", dpi=300)


