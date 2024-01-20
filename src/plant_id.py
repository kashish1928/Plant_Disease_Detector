import base64
import requests

API_KEY = 'LnlxIxlnhOT7396Rwdz9XZGeakodDd8ibz0dFtdnyjYduOpPci'

class Plant_ID:
    def __init__(self):
        pass

    """
    INPUT: Path to the image of plant to be identified
    OUTPUT: JSON object containing the result of the identification
    """
    def identify_plant(image_path):
        #Encode given image
        with open(image_path, 'rb') as file:
            images = [base64.b64encode(file.read()).decode('ascii')]

        #Post request to plant.id API
        response_identify = requests.post(
        'https://api.plant.id/v3/identification',
        params={'details': 'url,common_names'},
        headers={'Api-Key': API_KEY},
        json={'images': images})

        #Convert to JSon
        result = response_identify.json()
        if result['result']['is_plant']['binary']:
            return result
        else:
            return 0

    
    def health_assessment_plant(image_path):
        #Encode given image
        with open(image_path, 'rb') as file:
            images = [base64.b64encode(file.read()).decode('ascii')]

        #Post request to plant.id API
        response_health = requests.post(
        'https://api.plant.id/v3/health_assesment',
        params={'details': 'description,treatment'},
        headers={'Api-Key': API_KEY},
        json={'images': images},
        )   

        #Convert to JSon
        result = response_health.json()

        if result['result']['is_plant']['binary']:
            if result['result']['is_healthy']['binary']:
                return 1
            else:
                return result
        else:
            return 0
    
    """
    INPUT: JSON object containing the result of the identification
    OUTPUT: String Containgin Name of the plant
    """
    def get_plant_id(identification):
        return identification['result']['classification']['suggestions'][0]['id']

    def get_plant_name(identification):
        return identification['result']['classification']['suggestions'][0]['name']
    
    def get_plant_common_name(identification):
        return identification['result']['classification']['suggestions'][0]['common_name']
    
    
    def get_plant_url(identification):
        return identification['result']['classification']['suggestions'][0]['url']
    
    def get_plant_disease_status(health):
        return health['result']['binary']
    
    def get_disease_probability(health):
        return health['result']['disease']['suggestions'][0]['probability']

    def get_disease_name(health):
        return health['result']['disease']['suggestions'][0]['name']

    def get_disease_description(health):
        return health['result']['disease']['suggestions'][0]['details']['description']
    
    def get_disease_biological_treatment(health):
        return health['result']['disease']['suggestions'][0]['details']['treatment']['biological']
    
    def get_disease_chemical_treatment(health):
        return health['result']['disease']['suggestions'][0]['details']['treatment']['chemical']
    
    def get_disease_prevention(health):
        return health['result']['disease']['suggestions'][0]['details']['treatment']['prevention']


    
    