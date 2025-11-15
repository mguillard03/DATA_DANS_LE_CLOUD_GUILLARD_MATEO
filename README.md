# DATA_DANS_LE_CLOUD_GUILLARD_MATEO

# Projet Vélib Paris – Analyse et Visualisation

## 🔹 Description

Ce projet vise à analyser et visualiser les données des stations Vélib’ de Paris.  
Il utilise **MongoDB** pour stocker les données et **Python** pour effectuer les analyses et générer des cartes interactives.

Le projet inclut :  
- Import des données Vélib depuis l’API publique.  
- Stockage des données dans **MongoDB local** (problèmes rencontrés avec Atlas Free).  
- Analyse statistique globale et par commune.  
- Clustering des stations selon la disponibilité des vélos et des docks.  
- Régression linéaire pour prédire la capacité d’une station.  
- Cartes interactives avec Folium pour visualiser la disponibilité et les clusters.  
- Architecture prévue pour ajouter **Neo4J** dans une seconde partie du projet.

---

## 🔹 Architecture du projet

velib_project/
│  
├─ maps/  
│ └─ velib_clusters.html    
│ └─ velib_paris_map.html    
├─ scripts/  
│ ├─ import_velib.py  
│ └─ analyse_velib.py  
│ └─ carte_clusters_velib.py    
│ └─ carte_velib.py    
├─ README.md  
└─ requirements.txt  


---

## Installation et dépendances

Le projet utilise Python 3.10 et les packages suivants :

numpy
pandas
pymongo
scikit-learn
folium
requests

Installer avec pip :
  python -m venv venv
  venv\Scripts\activate  # Windows
  pip install -r requirements.txt


## Récupération et stockage des données

### Import depuis l’API Vélib :

Le script import_velib.py récupère toutes les stations (~1500) avec :
- Nombre de vélos disponibles (numbikesavailable)
- Nombre de places libres (numdocksavailable)
- Capacité totale (capacity)
- Type de vélos (mechanical / ebike)
- Localisation GPS

### MongoDB local :

- MongoDB Atlas Free a posé des problèmes SSL/TLS ; nous utilisons donc MongoDB local.
- Les données sont insérées dans la collection stations de la base velib_paris.


## 🔹 Analyse des données

Le script `analyse_velib.py` réalise les analyses suivantes :

### Statistiques globales
- **Nombre total de stations** : 1500
- **Vélos disponibles** : moyenne ≈ 12, min = 0, max = 73
- **Docks disponibles** : moyenne ≈ 19, min = 0, max = 100
- **Capacité totale** : moyenne ≈ 32, min = 0, max = 105

Quartiles pour vélos disponibles, docks et capacité :
- 25% : 4 vélos / 9 docks / 23 capacité  
- 50% : 9 vélos / 17 docks / 30 capacité  
- 75% : 18 vélos / 26 docks / 38 capacité

### Analyse par commune
Somme des vélos disponibles par arrondissement (top 10) :

| Commune                  | Vélos disponibles |
|---------------------------|-----------------|
| Paris                     | 11 920          |
| Issy-les-Moulineaux       | 508             |
| Boulogne-Billancourt      | 411             |
| Saint-Denis               | 343             |
| Ivry-sur-Seine            | 279             |
| Pantin                    | 244             |
| Asnières-sur-Seine        | 232             |
| Clichy                    | 227             |
| Vitry-sur-Seine           | 205             |
| Créteil                   | 179             |

### Clustering des stations (KMeans)
Classification selon `numbikesavailable` et `numdocksavailable`. Exemple de clusters :

| Cluster | Nb stations | Vélos moy | Docks moy | Capacité moy |
|---------|------------|------------|-----------|--------------|
| 0       | 474        | 6.76       | 14.10     | 21.80        |
| 1       | 97         | 40.55      | 10.27     | 51.75        |
| 2       | 164        | 7.37       | 42.71     | 50.91        |
| 3       | 341        | 20.90      | 6.43      | 28.37        |
| 4       | 424        | 6.52       | 26.45     | 33.83        |

- **Cluster 0** : peu de vélos et peu de docks  
- **Cluster 1** : beaucoup de vélos, peu de docks  
- **Cluster 2** : peu de vélos, beaucoup de docks  
- **Cluster 3** : moyenne disponibilité  
- **Cluster 4** : intermédiaire

### Régression linéaire
- Prédiction de la **capacité totale** à partir du nombre de vélos mécaniques et eBikes.
- **Coefficients** : `[0.52, 0.52]`  
- **Intercept** : `25.48`  
- **Score R²** : `≈ 0.20` (modèle simple, pas très prédictif mais montre une tendance)


---

## 🔹 Visualisation

Le script `carte_velib.py` crée des cartes interactives avec **Folium** :

- Points colorés selon vélos disponibles :  
  - 0-5 vélos → 🔴 rouge  
  - 6-10 vélos → 🟡 jaune  
  - + 10 vélos → 🟢 vert  

- Une deuxième carte peut afficher les **clusters** avec 5 couleurs distinctes.

> Les cartes sont sauvegardées en HTML dans le dossier `maps`.


## 🔹 Usage

1. **Lancer MongoDB local**  
   Assurez-vous que votre serveur MongoDB fonctionne sur votre machine (par défaut `mongodb://localhost:27017`).

2. **Récupérer les données**  
   Exécutez le script `import_velib.py` pour récupérer les données Vélib’ Paris depuis l’API et les insérer dans MongoDB local :  
   python import_velib.py  
   Ce script télécharge environ 1500 stations et les stocke dans la collection stations de la base velib_paris.

3. **Analyser les données**   
   python scripts/analyse_velib.py  
   Ce script fait des analyses sur les stations et des comparaisons entre clusters.

4. **Visualiser les cartes**  
   python maps/carte_velib.py  

   


