import requests
from pymongo import MongoClient

# Connexion MongoDB 
client = MongoClient("mongodb://localhost:27017/")
db = client["velib_paris"]
stations = db["stations"]

# Récupération des données depuis l’API Vélib’ Paris
url = "https://data.opendatasoft.com/api/records/1.0/search/"
params = {
    "dataset": "velib-disponibilite-en-temps-reel@parisdata",
    "rows": 1500
}

print("Récupération des données Vélib’ Paris...")
response = requests.get(url, params=params)
data = response.json()
records = data.get("records", [])

print(f"{len(records)} stations récupérées.")

# Sauvegarde dans MongoDB local
if records:
    stations.delete_many({})  # vide la collection
    stations.insert_many(records)
    print(f"{stations.count_documents({})} documents insérés dans MongoDB local.")
else:
    print("Pas de stations récupérées.")
