import pymongo
import plant_id
import json

class plantDiseaseQuery:
    def __init__(self):
        conn_str = "mongodb+srv://kashishjoshipura:ubc2026@cluster0.cty5my6.mongodb.net/?retryWrites=true&w=majority"
        try:
            client = pymongo.MongoClient(conn_str)
        except Exception:
            print("Error:" + Exception)
        myDb = client["plantDiseaseDetect"]
        plantTable = myDb["plantTable"]
        # Opening JSON file
        f = open('../data/data.json')
        
        # returns JSON object as 
        # a dictionary
        file_path = json.load(f)
        f.close()
        identification = file_path["Identification"]
        health = file_path["health"]
        aPlant = plant_id.Plant_ID()

        def add_plant(self):
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
                "prevention":aPlant.get_disease_prevention(health)
            }
            res = plantTable.insert_one(myPlant)

        def get_db_plantID(self):
            result = plantTable.find({}, {"plantID": 1, "_id": 0})
            return [item["plantID"] for item in result]
        
        def get_db_plantName(self):
            result = plantTable.find({}, {"plantName": 1, "_id": 0})
            return [item["plantName"] for item in result]
        
        def get_db_commonName(self):
            result = plantTable.find({}, {"commonName": 1, "_id": 0})
            return [item["commonName"] for item in result]
        
        def get_db_url(self):
            result = plantTable.find({}, {"url": 1, "_id": 0})
            return [item["url"] for item in result]
        
        def get_db_hasDisease(self):
            result = plantTable.find({}, {"hasDisease": 1, "_id": 0})
            return [item["hasDisease"] for item in result]
        
        def get_db_probability(self):
            result = plantTable.find({}, {"probability": 1, "_id": 0})
            return [item["probability"] for item in result]
        
        def get_db_diseaseName(self):
            result = plantTable.find({}, {"diseaseName": 1, "_id": 0})
            return [item["diseaseName"] for item in result]
        
        def get_db_probability(self):
            result = plantTable.find({}, {"description": 1, "_id": 0})
            return [item["description"] for item in result]
        
        def get_db_probability(self):
            result = plantTable.find({}, {"chemicalTreatment": 1, "_id": 0})
            return [item["chemicalTreatment"] for item in result]
        
        def get_db_probability(self):
            result = plantTable.find({}, {"biologicalTreatment": 1, "_id": 0})
            return [item["biologicalTreatment"] for item in result]
        
        def get_db_probability(self):
            result = plantTable.find({}, {"prevention": 1, "_id": 0})
            return [item["prevention"] for item in result]

