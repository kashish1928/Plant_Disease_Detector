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
conn_str = "mongodb+srv://kashishjoshipura:ubc2026@cluster0.cty5my6.mongodb.net/?retryWrites=true&w=majority"
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

# Opening JSON file
f = open('./data/data.json')
 
# returns JSON object as 
# a dictionary
file_path = json.load(f)

f.close()

im = Image.open("src/images/test.jpg")

image_bytes = io.BytesIO()
im.save(image_bytes, format='JPEG')

image = image_bytes.getvalue()

identification = file_path["Identification"]
print(type(identification))
aPlant = plant_id.Plant_ID()
myPlant = {
    "plantID":aPlant.get_plant_id(identification),
    "plantName":aPlant.get_plant_name(file_path["Identification"]),
    "commonName":aPlant.get_plant_common_name(file_path["Identification"]),
    "url":aPlant.get_plant_url(file_path["Identification"]),
    "hasDisease": aPlant.get_plant_disease_status(file_path["health"]),
    "probability":aPlant.get_disease_probability(file_path["health"]),
    "diseaseName":aPlant.get_disease_name(file_path["health"]),
    "description":aPlant.get_disease_description(file_path["health"]),
    "chemicalTreatment":aPlant.get_disease_chemical_treatment(file_path["health"]),
    "biologicalTreatment":aPlant.get_disease_biological_treatment(file_path["health"]),
    "prevention":aPlant.get_disease_prevention(file_path["health"]),
    "image":image
}

# STEP 6 : Insert the document
res = plantTable.insert_one(myPlant)

# STEP 7 : Read the document
record = plantTable.find_one()
print(record)

pil_img = Image.open(io.BytesIO(record['image']))
plt.imshow(pil_img)
plt.show()