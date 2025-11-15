import pandas as pd
import folium
from pymongo import MongoClient

# -------------------------------------------------------------------
# Connexion à MongoDB 
# -------------------------------------------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["velib_paris"]
stations = db["stations"]

# -------------------------------------------------------------------
# Charger les données dans un DataFrame
# -------------------------------------------------------------------
data = list(stations.find({}, {"_id": 0, "fields": 1}))
df = pd.json_normalize([item["fields"] for item in data])

# Extraire latitude et longitude
df["lat"] = df["coordonnees_geo"].apply(lambda x: x[0])
df["lon"] = df["coordonnees_geo"].apply(lambda x: x[1])

# -------------------------------------------------------------------
# Fonction pour attribuer une couleur selon le nombre de vélos dispo
# -------------------------------------------------------------------
def bike_color(n):
    if n <= 5:
        return "red"
    elif n <= 10:
        return "yellow"
    else:
        return "green"

# -------------------------------------------------------------------
# Création de la carte centrée sur Paris
# -------------------------------------------------------------------
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Ajouter les stations
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=6,
        color=bike_color(row["numbikesavailable"]),
        fill=True,
        fill_color=bike_color(row["numbikesavailable"]),
        fill_opacity=0.7,
        popup=f"{row['name']}\nVélos dispo : {row['numbikesavailable']}"
    ).add_to(m)

# -------------------------------------------------------------------
# Ajouter une légende
# -------------------------------------------------------------------
legend_html = """
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 120px; 
     background-color: white; z-index:9999; font-size:14px;
     border:2px solid grey; padding: 10px;">
     <b>Vélos disponibles</b><br>
     <i><span style="color:red;">●</span> 0-5</i><br>
     <i><span style="color:orange;">●</span> 6-10</i><br>
     <i><span style="color:green;">●</span> >10</i>
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# -------------------------------------------------------------------
# Sauvegarder la carte
# -------------------------------------------------------------------
m.save("velib_paris_map.html")
print("Carte générée : velib_paris_map.html")
