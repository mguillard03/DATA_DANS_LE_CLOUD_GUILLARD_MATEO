import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

# -------------------------------------------------------------------
# Connexion MongoDB 
# -------------------------------------------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["velib_paris"]
stations = db["stations"]

print("\n=== ANALYSE VÉLIB PARIS ===\n")

# -------------------------------------------------------------------
# Charger les données dans un DataFrame
# -------------------------------------------------------------------
data = list(stations.find({}, {"_id": 0, "fields": 1}))
df = pd.json_normalize([item["fields"] for item in data])

print("Nombre total de stations :", len(df))

# -------------------------------------------------------------------
# STATISTIQUES DE BASE
# -------------------------------------------------------------------
print("\n--- Statistiques globales ---")
print(df[["numbikesavailable", "numdocksavailable", "capacity"]].describe())

# -------------------------------------------------------------------
# ANALYSE PAR COMMUNE
# -------------------------------------------------------------------
print("\n--- Nombre de vélos par commune ---")
group_commune = df.groupby("nom_arrondissement_communes")["numbikesavailable"].sum()
print(group_commune.sort_values(ascending=False).head(10))

# -------------------------------------------------------------------
# CLUSTERING (KMeans)
# -------------------------------------------------------------------
print("\n--- Clustering des stations selon disponibilité ---")
X = df[["numbikesavailable", "numdocksavailable"]].values

kmeans = KMeans(n_clusters=5, random_state=0, n_init=10)
df["cluster"] = kmeans.fit_predict(X)

print(df[["name", "numbikesavailable", "numdocksavailable", "cluster"]].head())

# -------------------------------------------------------------------
# COMPARAISON DES CLUSTERS
# -------------------------------------------------------------------
cluster_summary = df.groupby("cluster").agg(
    nb_stations=("name", "count"),
    velos_moy=("numbikesavailable", "mean"),
    docks_moy=("numdocksavailable", "mean"),
    capacity_moy=("capacity", "mean")
)

print("\n--- Comparaison des clusters ---")
print(cluster_summary)

# -------------------------------------------------------------------
# RÉGRESSION LINÉAIRE (prédire la capacité)
# -------------------------------------------------------------------
print("\n--- Régression linéaire : prédire la capacité ---")
X_reg = df[["mechanical", "ebike"]].fillna(0)
y = df["capacity"]

model = LinearRegression()
model.fit(X_reg, y)

print("Coefficients :", model.coef_)
print("Intercept :", model.intercept_)
print("Score R² :", model.score(X_reg, y))
