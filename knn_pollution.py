import warnings; warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline


#  Fonctions


def find_col(df: pd.DataFrame, needle: str) -> str:
    """Retourne le 1er nom de colonne contenant ‹ needle › (casse ignorée)."""
    hits = [c for c in df.columns if needle.lower() in c.lower()]
    if not hits:
        raise KeyError(f"Aucune colonne contenant « {needle} » trouvée.")
    return hits[0]


def clean_name(s: str) -> str:
    """Nettoie un nom de station pour l'alignement (majuscules, trim)."""
    if pd.isna(s):
        return ""
    return " ".join(s.strip().upper().split())


# On va charger les deux fichiers

CSV_BASE = "stations_metro_propre.csv"
CSV_AIR = "qualite-de-lair-dans-le-reseau-de-transport-francilien.csv"
classes = ["pollution faible", "pollution moyenne", "pollution élevée"]

df_base = pd.read_csv(CSV_BASE)
df_air = pd.read_csv(CSV_AIR, sep=";")


#  Détection et renommage des colonnes importantes

col_station_air = find_col(df_air, "station")
col_ligne_air = find_col(df_air, "ligne")

df_air = df_air.rename(columns={
    col_station_air: "Nom station air",
    col_ligne_air: "Nom ligne air"
})


#  Enrichissement du CSV air


df_air = df_air[df_air["Nom ligne air"].str.contains("métro", case=False, na=False)]



df_air["incertitude_forte"] = df_air["Incertitude"].str.contains("forte", case=False, na=False).astype(int)
df_air["station_aerienne"] = df_air["Incertitude"].str.contains("aérienne", case=False, na=False).astype(int)
df_air["surveillance"] = df_air["Recommandation de surveillance"].notna().astype(int)



df_air = pd.get_dummies(df_air, columns=["Nom ligne air"], prefix="ligne", drop_first=True)





df_base["Nom clean"] = df_base["Nom de la Station"].apply(clean_name)
df_air["Nom clean"] = df_air["Nom station air"].apply(clean_name)

feature_cols_extra = [
    "incertitude_forte",
    "station_aerienne",
    "surveillance",
] + [c for c in df_air.columns if c.startswith("ligne_")]

df = df_base.merge(
    df_air[["Nom clean"] + feature_cols_extra],
    on="Nom clean",
    how="left",
)

df[feature_cols_extra] = df[feature_cols_extra].fillna(0)

df = df[df["niveau_pollution"].isin(classes)].copy()


#  Préparation de x et y


X = df[["stop_lat", "stop_lon"] + feature_cols_extra].values
y = df["niveau_pollution"].values


#  Train / test, séparation


X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42
)


#  Pipeline et GridSearchCV


pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("smote", SMOTE(random_state=42, k_neighbors=2)),
    ("knn", KNeighborsClassifier()),
])

param_grid = {
    "knn__n_neighbors": [3, 5, 7, 9],
    "knn__weights": ["uniform", "distance"],
    "knn__metric": ["euclidean", "manhattan"],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

gs = GridSearchCV(pipe, param_grid, cv=cv, scoring="f1_macro", n_jobs=-1).fit(X_tr, y_tr)

print("\nMeilleurs hyper‑paramètres :", gs.best_params_)
print("F1_macro (cross‑val)      :", round(gs.best_score_, 3))

best = gs.best_estimator_
y_pred = best.predict(X_te)


#  Rapport et la matrice


report_df = (
    pd.DataFrame(classification_report(y_te, y_pred, target_names=classes, output_dict=True))
    .T.loc[classes]
    .round(3)
)

cm = confusion_matrix(y_te, y_pred, labels=classes)
cm_df = pd.DataFrame(
    cm,
    index=classes,
    columns=[f"préd_{c.split()[-1]}" for c in classes],
)

resultats = pd.concat([report_df, cm_df], axis=1)

print("\n===== Rapport + Confusion côte à côte =====")
print(resultats.to_string())


#  Le heatmap 


plt.figure(figsize=(5, 4))
plt.imshow(cm, cmap="plasma")
plt.colorbar(label="Nombre de prédictions")
plt.xticks(range(3), [c.split()[-1] for c in classes], rotation=45)
plt.yticks(range(3), [c.split()[-1] for c in classes])
plt.xlabel("Prédictions"); plt.ylabel("Réalité")
plt.title("Matrice de confusion – K‑NN enrichi")
for i in range(3):
    for j in range(3):
        plt.text(j, i, cm[i, j], ha="center", va="center", color="white")
plt.tight_layout()
plt.savefig("graph_knn_confusion.png", dpi=300)


