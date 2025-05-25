
library(readr)
library(dplyr)
library(magrittr) 


# Lecture du fichier CSV avec point-virgule comme séparateur
data <- read_delim("qualite-de-lair-dans-le-reseau-de-transport-francilien.csv", delim = ";")

# Afficher les noms de colonnes pour vérification
names(data)

#Nettoyage dataset en remplaçant les chaînes vides par NA
data[data == ""] <- NA

# On va supprimer les lignes où toutes les valeurs sont NA 
data <- data[rowSums(is.na(data)) != ncol(data), ]

# On va supprimer les colonnes où toutes les valeurs sont NA
data <- data[, colSums(is.na(data)) != nrow(data)]

# On va supprimer les lignes en double 
data <- unique(data)


#filtrer dataset
metro_data <- data[grepl("Métro", data$`Nom de la ligne`),ignore.case = TRUE, ]

set.seed(123)
indices <- sample(1:nrow(metro_data))
split_point <- floor(0.7 * nrow(metro_data))
train <- metro_data[indices[1:split_point], ]
test <- metro_data[indices[(split_point + 1):nrow(metro_data)], ]
write.csv(metro_data, "stations_metro_propre.csv", row.names = FALSE)



