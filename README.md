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
  - plus 10 vélos → 🟢 vert  

<img width="1888" height="873" alt="image" src="https://github.com/user-attachments/assets/0bac706b-4739-4943-9148-4884fbefb91e" />

- Une deuxième carte peut afficher les **clusters** avec 5 couleurs distinctes.

<img width="1577" height="900" alt="image" src="https://github.com/user-attachments/assets/9eb7f197-2617-4da3-aaf1-73e728396698" />

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



# Projet Neo4J – Game of Thrones

Base de données graphe autour des personnages, maisons et batailles

---

## 1. Contexte

Ce projet a pour objectif de modéliser une partie de l’univers de *Game of Thrones* au sein d’une base de données Neo4j.
Nous utilisons une approche orientée graphe pour représenter :

* les maisons (Houses)
* les personnages (Characters)
* les batailles (Battles)
* les relations d’allégeance, de participation à une bataille, ou encore d’événements comme la mort d’un personnage.

---

## 2. Jeux de données utilisés

Les données proviennent d’un dépôt public GitHub :

* **battles.csv**
  Inclut : nom de la bataille, année, rois attaquants/défenseurs, tailles d’armée, localisation…

* **character-deaths.csv**
  Inclut : nom du personnage, allégeance, année de mort, chapitres, niveau de noblesse…

Fichiers disponibles ici :
`./Data/battles.csv`
`./Data/character-deaths.csv`

---

## 3. Modélisation du graphe

### Nœuds

| Label       | Description                                    |
| ----------- | ---------------------------------------------- |
| `Character` | Un personnage du monde de GoT                  |
| `House`     | Une maison à laquelle un personnage appartient |
| `Battle`    | Un événement militaire                         |

### Relations

| Relation                               | Description                                  |
| -------------------------------------- | -------------------------------------------- |
| `(:Character)-[:BELONGS_TO]->(:House)` | Le personnage jure fidélité à une maison     |
| `(:House)-[:ATTACKED]->(:Battle)`      | La maison a attaqué lors de cette bataille   |
| `(:House)-[:DEFENDED]->(:Battle)`      | La maison a défendu lors de cette bataille   |
| `(:Character)-[:DIED_IN]->(:Battle)`   | Le personnage est mort durant cette bataille |

---

## Diagramme du modèle

<img width="701" height="712" alt="image" src="https://github.com/user-attachments/assets/e127ea09-bd6f-45fb-abc1-77ed83b29237" />

---

## 4. Import dans Neo4j Aura

### Pré-requis

Neo4j Aura nécessite que les CSV soient publiquement accessibles via HTTPS.

### Création des nœuds House

```cypher
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mguillard03/DATA_DANS_LE_CLOUD_GUILLARD_MATEO/main/Data/character-deaths.csv" AS row
WITH DISTINCT row.Allegiances AS house WHERE house <> 'None' AND house IS NOT NULL
CREATE (:House {name: house});
```

### Création des nœuds Character et appartenance

```cypher
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mguillard03/DATA_DANS_LE_CLOUD_GUILLARD_MATEO/main/Data/character-deaths.csv" AS row
MERGE (c:Character {name: row.Name})
WITH c, row
WHERE row.Allegiances <> 'None' AND row.Allegiances IS NOT NULL
MATCH (h:House {name: row.Allegiances})
MERGE (c)-[:BELONGS_TO]->(h);
```
<img width="527" height="633" alt="image" src="https://github.com/user-attachments/assets/d041ea62-3afd-4086-b658-20c9a2563a43" />

### Création des nœuds Battle

```cypher
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mguillard03/DATA_DANS_LE_CLOUD_GUILLARD_MATEO/main/Data/battles.csv" AS row
CREATE (:Battle {
  name: row.name,
  year: toInteger(row.year),
  attacker_king: row.attacker_king,
  defender_king: row.defender_king
});
```

### Relations ATTACKED & DEFENDED

```cypher
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mguillard03/DATA_DANS_LE_CLOUD_GUILLARD_MATEO/main/Data/battles.csv" AS row
MATCH (b:Battle {name: row.name})
UNWIND [row.attacker_1, row.attacker_2, row.attacker_3, row.attacker_4] AS atk
WITH b, atk WHERE atk IS NOT NULL AND atk <> ""
MATCH (h:House {name: atk})
MERGE (h)-[:ATTACKED]->(b);
```
<img width="542" height="502" alt="image" src="https://github.com/user-attachments/assets/555b321e-1b48-48f9-a447-ffc861fa3b50" />


```cypher
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mguillard03/DATA_DANS_LE_CLOUD_GUILLARD_MATEO/main/Data/battles.csv" AS row
MATCH (b:Battle {name: row.name})
UNWIND [row.defender_1, row.defender_2, row.defender_3, row.defender_4] AS def
WITH b, def WHERE def IS NOT NULL AND def <> ""
MATCH (h:House {name: def})
MERGE (h)-[:DEFENDED]->(b);
```
<img width="552" height="485" alt="image" src="https://github.com/user-attachments/assets/057a1430-ac22-4059-baf0-f6f00aa72209" />


### Relation DIED_IN

```cypher
MATCH (c:Character) WHERE c.DeathYear IS NOT NULL
MATCH (b:Battle)
WHERE b.year = c.DeathYear
MERGE (c)-[:DIED_IN]->(b);
```

---

## 5. Requêtes utiles

### Maisons les plus impliquées dans des batailles

```cypher
MATCH (h:House)-[r]->(b:Battle)
RETURN h.name AS house, type(r) AS role, count(*) AS occurrences
ORDER BY occurrences DESC;
```
<img width="910" height="565" alt="image" src="https://github.com/user-attachments/assets/9eae782e-0bfc-462a-8747-f7e32341402e" />


---

### Personnages par maison

```cypher
MATCH (h:House)<-[:BELONGS_TO]-(c:Character)
RETURN h.name AS house, collect(c.name) AS members;
```

<img width="1093" height="487" alt="image" src="https://github.com/user-attachments/assets/742c7cab-702b-4d87-9b57-b1c6eec3fc1f" />


---

### Batailles avec le plus de participants

```cypher
MATCH (h)-[:ATTACKED|DEFENDED]->(b:Battle)
RETURN b.name AS battle, count(h) AS houses
ORDER BY houses DESC;
```

<img width="412" height="587" alt="image" src="https://github.com/user-attachments/assets/f5db3c0a-2fdc-407c-b034-4f8a117dd0a5" />

---

## 6. Export de la base (AuraDB)

```cypher
CALL apoc.export.cypher.all(null, {stream:true, format:'cypher-shell'})
YIELD cypherStatements
RETURN cypherStatements;
```

Fichier exporté :
`./Data/metadonnee_neo4j_GOT.csv`

---

## 7. Auteur

Projet réalisé pour le module *Data dans le cloud* à Sup De Vinci
Par Guillard Mateo


---





   


