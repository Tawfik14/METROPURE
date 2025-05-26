
library(readr)
library(dplyr)
library(magrittr)
library(sf)
library(leaflet)
library(ggplot2)
library(viridis)
library(htmlwidgets) 
library(class)

# Lecture du fichier CSV avec point-virgule comme séparateur
data <- read_delim("qualite-de-lair-dans-le-reseau-de-transport-francilien (1).csv", delim = ";")

# Afficher les noms de colonnes pour vérification
names(data)

#Nettoyage dataset
# Remplacer les chaînes vides par NA
data[data == ""] <- NA

# Supprimer les lignes où toutes les valeurs sont NA (cette commande ne fait rien car pas de lignes inutiles)
data <- data[rowSums(is.na(data)) != ncol(data), ]

# Supprimer les colonnes où toutes les valeurs sont NA
data <- data[, colSums(is.na(data)) != nrow(data)]

# Supprimer les lignes en double 
# Supprimer colonne niveau car pareil que colonne niveau_pollution
data$niveau <- NULL


# essai de ACP
summary(data)
str(data)

acp = prcomp(data, scale. = TRUE)
summary(acp)
biplot(acp)

# pas de ACP possible car il y a que trois colonnes numeriques utiles. Les autres sont qualitatives
# DE plus ACP necessite plusieurs variables numeriques correlées

# = ACP n'apportera pas d'informations supplémentaires

#filtrer dataset
metro_data <- data[grepl("Métro", data$`Nom de la ligne`),ignore.case = TRUE, ]

#construction des deux nouveaux fichiers
set.seed(123)
indices <- sample(1:nrow(metro_data))
split_point <- floor(0.7 * nrow(metro_data))
train <- metro_data[indices[1:split_point], ]
test <- metro_data[indices[(split_point + 1):nrow(metro_data)], ]
write.csv(metro_data, "stations_metro_propre.csv", row.names = FALSE)


# k -means pour predire la pollution

# QUESTION 5

#Sélection et nettoyage
df <- data %>%
  select('Nom de la Station', stop_lat, stop_lon, niveau_pollution) %>%
  filter(!is.na(stop_lat), !is.na(stop_lon)) %>%
  mutate(niveau_pollution = tolower(niveau_pollution)) %>%
  filter(niveau_pollution %in% c("pollution faible", "pollution moyenne", "pollution forte"))

#  Encodage en facteur numérique 
df$pollution_num <- as.numeric(factor(df$niveau_pollution,
                                      levels = c("pollution faible", "pollution moyenne", "pollution forte")))

#  Standardisation des variables pour clustering
df_scaled <- scale(df[, c("stop_lat", "stop_lon")])

#  Clustering k-means (on impose 3 groupes) 
set.seed(42)
km <- kmeans(df_scaled, centers = 3, nstart = 25)

# Ajout des clusters au dataframe 
df$cluster <- as.factor(km$cluster)

# Visualisation
ggplot(df, aes(x = stop_lon, y = stop_lat, color = cluster)) +
  geom_point(size = 2) +
  labs(title = "Clustering géographique des stations selon pollution",
       x = "Longitude", y = "Latitude", color = "Cluster") +
  theme_minimal()




#QUESTION 6

# Encoder les variables catégorielles
metro_data <- metro_data %>%
  filter(niveau_pollution %in% c("pollution faible", "pollution moyenne", "pollution élevée"))

# Encodage ligne de métro
metro_data$ligne_encoded <- as.numeric(as.factor(metro_data$`Nom de la ligne`))

# Encodage niveau de pollution (1 = élevée, 2 = moyenne, 3 = faible)
niveau_levels <- c("pollution élevée", "pollution moyenne", "pollution faible")
metro_data$pollution_encoded <- as.numeric(factor(metro_data$niveau_pollution, levels = niveau_levels))

#  Préparer X ( et y 
X <- data.frame(
  lon = metro_data$stop_lon,
  lat = metro_data$stop_lat,
  ligne = metro_data$ligne_encoded
)
y <- metro_data$pollution_encoded

#  Diviser en jeu d'entraînement et de test (70/30) car ici on veut créer un graphique
set.seed(123)
train_indices <- sample(1:nrow(X), size = 0.7 * nrow(X))
X_train <- X[train_indices, ]
X_test  <- X[-train_indices, ]
y_train <- y[train_indices]
y_test  <- y[-train_indices]

# Appliquer le modèle k-NN
k <- 5
y_pred <- knn(train = X_train, test = X_test, cl = y_train, k = k)

# Évaluer la performance
conf_mat <- table(Prediction = y_pred, Réalité = y_test)
accuracy <- sum(diag(conf_mat)) / sum(conf_mat)

# Afficher les résultats
print(conf_mat)
cat("\nPrécision du modèle k-NN :", round(accuracy * 100, 2), "%\n")

#  Ajouter les colonnes y_test et y_pred dans les données test
X_test$pollution_reelle <- factor(y_test, levels = c(1, 2, 3), labels = c("Élevée", "Moyenne", "Faible"))
X_test$pollution_predite <- factor(y_pred, levels = c(1, 2, 3), labels = c("Élevée", "Moyenne", "Faible"))

# Affichage graphique
ggplot(X_test, aes(x = lon, y = lat, color = pollution_predite)) +
  geom_point(size = 3) +
  labs(
    title = "Pollution prédite par k-NN",
    x = "Longitude",
    y = "Latitude",
    color = "Niveau prédit"
  ) +
  theme_minimal()


#créer carte avec qsis
# Vérifier les valeurs uniques du niveau de pollution
unique(data$niveau)

# Supprimer les lignes sans pollution mesurée
data_clean <- data %>%
  filter(!niveau %in% c("Pas de données", "Station aérienne")) %>%
  filter(!is.na(stop_lon), !is.na(stop_lat))

# Conversion en objet spatial

metro_sf <- st_as_sf(data_clean, coords = c("stop_lon", "stop_lat"), crs = 4326)

# Carte statique avec ggplot2


ggplot(metro_sf) +
  geom_sf(aes(color = niveau), size = 3) +
  scale_color_viridis_d(option = "D", end = 0.9) +
  theme_minimal() +
  labs(
    title = "Niveau de pollution par station de métro (Île-de-France)",
    color = "Pollution"
  )

#créer carte interactive avec qsis
# Renommer les colonnes (s'il y a des espaces)
names(metro_sf) <- gsub(" ", "_", names(metro_sf))

# Créer la palette de couleurs
pal <- colorFactor(
  palette = "YlOrRd",
  domain = as.character(metro_sf$niveau)
)

# Construire la carte avec titre, légende et échelle
m <- leaflet(metro_sf) %>%
  addTiles() %>%
  addControl(  # Titre
    html = "<strong style='font-size:16px;'>Niveau de pollution par station de métro (Île-de-France)</strong>",
    position = "topright"
  ) %>%
  addCircleMarkers(
    radius = 6,
    color = ~pal(niveau),
    label = ~paste(
      "Station :", Nom_de_la_Station,
      "<br>Ligne :", Nom_de_la_ligne,
      "<br>Pollution :", niveau
    ),
    fillOpacity = 0.8,
    stroke = FALSE
  ) %>%
  addLegend(
    position = "bottomright",
    pal = pal,
    values = ~niveau,
    title = "Niveau de pollution"
  ) %>%
  addScaleBar(  # Échelle en bas à gauche
    position = "bottomleft",
    options = scaleBarOptions(
      metric = TRUE, imperial = FALSE,
      updateWhenIdle = TRUE
    )
  )

# Sauvegarder et ouvrir dans le navigateur
saveWidget(m, "carte.html", selfcontained = TRUE)
browseURL("carte.html")



