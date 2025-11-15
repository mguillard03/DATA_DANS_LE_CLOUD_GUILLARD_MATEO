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

Le script `analyse_velib.py` réalise :

### Statistiques globales
- Moyenne, min, max, quartiles pour vélos disponibles, docks et capacité.

### Analyse par commune
- Somme des vélos disponibles par arrondissement.

### Clustering des stations (KMeans)
- Classification selon `numbikesavailable` et `numdocksavailable`.

Exemple de clusters :
- **Cluster 0** : peu de vélos et peu de docks  
- **Cluster 1** : beaucoup de vélos, peu de docks  
- **Cluster 2** : peu de vélos, beaucoup de docks  
- **Cluster 3** : moyenne disponibilité  
- **Cluster 4** : intermédiaire  

### Régression linéaire
- Prédiction de la capacité à partir du nombre de vélos mécaniques et eBikes.  
- Score R² ≈ 0.20 (modèle simple).

---

## 🔹 Visualisation

Le script `carte_velib.py` crée des cartes interactives avec **Folium** :

- Points colorés selon vélos disponibles :  
  - 0-5 vélos → 🔴 rouge  
  - 6-10 vélos → 🟡 jaune  
  - >10 vélos → 🟢 vert  

- Une deuxième carte peut afficher les **clusters** avec 5 couleurs distinctes.

> Les cartes sont sauvegardées en HTML dans le dossier `maps` et peuvent être ouvertes dans n’importe quel navigateur.

