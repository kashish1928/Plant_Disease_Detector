import base64
import requests
import json

API_KEY = 'LnlxIxlnhOT7396Rwdz9XZGeakodDd8ibz0dFtdnyjYduOpPci'

class Plant_ID:
    def __init__(self):
        pass

    """
    INPUT: Path to the image of plant to be identified
    OUTPUT: JSON object containing the result of the identification
    """
    def identify_plant(self,image_path):
        #Encode given image
        with open(image_path, 'rb') as file:
            images = [base64.b64encode(file.read()).decode('ascii')]

        response_identify = requests.post(
            'https://api.plant.id/v3/identification',
            params={'details': 'url,common_names'},
            headers={'Api-Key': API_KEY},
            json={'images': images},
        )

        #Convert to JSon
        print(response_identify.text)
        result = json.loads(response_identify.text)

        if result['result']['is_plant']['binary']:
            return result
        else:
            return 0

    
    def health_assessment_plant(self,image_path):
        #Encode given image
        with open(image_path, 'rb') as file:
            images = [base64.b64encode(file.read()).decode('ascii')]

        #Post request to plant.id API
        response_health = requests.post(
        'https://api.plant.id/v3/health_assessment',
        params={'details': 'description,treatment'},
        headers={'Api-Key': API_KEY},
        json={'images': images},
        )   

        #Convert to JSon
        print(response_health.text)
        result = json.loads(response_health.text)

        if result['result']['is_plant']['binary']:
            return result
        else:
            return 0
    
    """
    INPUT: JSON object containing the result of the identification
    OUTPUT: String Containgin Name of the plant
    """
    def get_plant_id(self,identification):
        return identification['result']['classification']['suggestions'][0]['id']

    def get_plant_name(self,identification):
        return identification['result']['classification']['suggestions'][0]['name']
    
    def get_plant_common_name(self,identification):
        return identification['result']['classification']['suggestions'][0]['details']['common_names']
    
    
    def get_plant_url(self,identification):
        return identification['result']['classification']['suggestions'][0]['details']['url']
    
    def get_plant_disease_status(self,health):
        return health['result']['is_healthy']['binary']
    
    def get_disease_probability(self,health):
        return health['result']['disease']['suggestions'][0]['probability']

    def get_disease_name(self,health):
        return health['result']['disease']['suggestions'][0]['name']

    def get_disease_description(self,health):
        return health['result']['disease']['suggestions'][0]['details']['description']
    
    def get_disease_biological_treatment(self,health):
        return health['result']['disease']['suggestions'][0]['details']['treatment']['biological']
    
    def get_disease_chemical_treatment(self,health):
        try:
            return health['result']['disease']['suggestions'][0]['details']['treatment']['chemical']
        except KeyError:
            return ["No chemical treatment available"]
    def get_disease_prevention(self,health):
        return health['result']['disease']['suggestions'][0]['details']['treatment']['prevention']
    
    def get_disease_image(self,identification):
        return identification['input']['images'][0]


    
    