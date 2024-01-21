# STEP 1 : Install and import necessary files
import pymongo
import plant_id
import json
from pymongo import MongoClient
from PIL import Image
import io
from bson.binary import Binary
import matplotlib.pyplot as plt

# STEP 2 : Create a mongodb client
conn_str = "CONNECTION TO YOUR MONGODB SERVER"
try:
    client = pymongo.MongoClient(conn_str)
except Exception:
    print("Error:" + Exception)
# client = pymongo.MongoClient()
    
# STEP 3 : Create a database
myDb = client["plantDiseaseDetect"]
# List databases
print(client.list_database_names())

# STEP 4 : Create a collection i.e table
plantTable = myDb["plantTable"]

# STEP 5 : Create a document/record

aPlant = plant_id.Plant_ID()
file_path = "src/images/Healthy.png"
identification = aPlant.identify_plant(file_path)
health = aPlant.health_assessment_plant(file_path)
print(identification)
print(health)

im = Image.open(file_path)

image_bytes = io.BytesIO()
im.save(image_bytes, format='PNG')

image = image_bytes.getvalue()

myPlant = {
    "plantID":aPlant.get_plant_id(identification),
    "plantName":aPlant.get_plant_name(identification),
    "commonName":aPlant.get_plant_common_name(identification),
    "url":aPlant.get_plant_url(identification),
    "hasDisease": aPlant.get_plant_disease_status(health),
    "probability":aPlant.get_disease_probability(health),
    "diseaseName":aPlant.get_disease_name(health),
    "description":aPlant.get_disease_description(health),
    "chemicalTreatment":aPlant.get_disease_chemical_treatment(health),
    "biologicalTreatment":aPlant.get_disease_biological_treatment(health),
    "prevention":aPlant.get_disease_prevention(health),
    "image":image
}

# STEP 6 : Insert the document
res = plantTable.insert_one(myPlant)

# STEP 7 : Read the document
record = plantTable.find_one()
print(record)