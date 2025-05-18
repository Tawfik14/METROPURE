
library(readr)
library(dplyr)
library(magrittr) 


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

# Supprimer les lignes en double ( de même elle ne fait rien on le remarque car le dataset n'espas modifier)
data <- unique(data)

#acp
#summary(data)
#str(data)

#acp=prcomp(data, scale. = TRUE)
#summary(acp)
#biplot(acp)

#filtrer dataset
metro_data <- data[grepl("Métro", data$`Nom de la ligne`),ignore.case = TRUE, ]

set.seed(123)
indices <- sample(1:nrow(metro_data))
split_point <- floor(0.7 * nrow(metro_data))
train <- metro_data[indices[1:split_point], ]
test <- metro_data[indices[(split_point + 1):nrow(metro_data)], ]



