import pandas as pd
import folium
from pymongo import MongoClient
from sklearn.cluster import KMeans

# Connexion MongoDB 
client = MongoClient("mongodb://localhost:27017/")
db = client["velib_paris"]
stations = db["stations"]

# Charger les données dans un DataFrame
data = list(stations.find({}, {"_id": 0, "fields": 1}))
df = pd.json_normalize([item["fields"] for item in data])

# Vérifier les coordonnées
df = df.dropna(subset=["coordonnees_geo"])
df[["lat", "lon"]] = pd.DataFrame(df["coordonnees_geo"].tolist(), index=df.index)

# Clustering (KMeans) sur la position géographique
X_geo = df[["lat", "lon"]].values
kmeans_geo = KMeans(n_clusters=5, random_state=0, n_init=10)
df["geo_cluster"] = kmeans_geo.fit_predict(X_geo)

# Couleurs pour chaque cluster
colors = ["red", "orange", "green", "blue", "purple"]

# Créer la carte centrée sur Paris
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Ajouter les stations
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color=colors[row["geo_cluster"]],
        fill=True,
        fill_opacity=0.7,
        popup=f"{row['name']}<br>Vélos dispo: {row['numbikesavailable']}"
    ).add_to(m)

# Ajouter légende
legend_html = """
<div style="
    position: fixed;
    bottom: 50px; left: 50px; width: 180px; height: 130px;
    background-color: white; z-index:9999; font-size:14px;
    border:2px solid grey; padding: 10px;">
<b>Clusters géographiques</b><br>
<i style="color:red;">● Cluster 0</i><br>
<i style="color:orange;">● Cluster 1</i><br>
<i style="color:green;">● Cluster 2</i><br>
<i style="color:blue;">● Cluster 3</i><br>
<i style="color:purple;">● Cluster 4</i>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Sauvegarder la carte
m.save("velib_clusters.html")
print("Carte des clusters sauvegardée dans velib_clusters.html")
