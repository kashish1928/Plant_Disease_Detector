#imports
from taipy.gui import Gui, State, notify
import taipy.gui.builder as tgb
import openai
from PIL import Image
import io
import base64
import plantDiseaseQuery
import matplotlib.pyplot as plt
import plant_id
import pandas as pd

#initialize variables

#Plant Dashboard vars
plant_name = ""
Common_Name = ""
Healthy = ""
Chance = ""
Disease_Name = ""
Disease_Description = ""
Chemical_Treatment = ""
Biological_Treatment = ""
Prevention = ""


# initialised dictionary and context storing the conversation history
context = f"I've just adopted a plant and it's name is {plant_name}"
conversation = {
    "Conversation": [f"I've just adopted a plant and I would like to know more about it", "Hi! I can take a look at it and tell you about it."]
}
current_user_message = ""
past_conversations = []

current_image = "src/images/template.png"

#message that user will type
def image_resize():
    current_image = "src/saved/fixed_img.png"
    image = Image.open(current_image)
    new_image = image.resize((1000, 1000))
    new_image.save(current_image)

image_resize()

#api call
client = openai.Client(api_key="YOUR OPEN AI KEY")


#functions to api

def request4(state: State, prompt: str) -> str:
    """
    Send a prompt to the GPT-4 API and return the response.

    Args:
        - state: The current state.
        - prompt: The prompt to send to the API.

    Returns:
        The response from the API.
    """
    response = state.client.chat.completions.create(
        messages=[   {
            "role": "user",
            "content": "GPT, your task is to identify the type of plant and identify that plant health issues with precision. If a condition is unrecognizable, reply with \'I don\'t know\'. Analyze any image of a plant or leaf I provide, and detect all abnormal conditions, whether they are diseases, pests, deficiencies, or decay. Respond strictly with the name of the condition identified, and nothing else—no explanations, no additional text. If a condition is unrecognizable, reply with \'I don\'t know\'. If the image is not plant-related, say \'Please pick another image\'"  # Content is a string
        },
            {
                "role": "user",
                "content":[ {
                'type': 'image_url',
                'image_url': {
                    "url": f"data:image/jpeg;base64,{prompt}"
                },
              }],
            }
        ],
        model="gpt-4-vision-preview",
    )
    return response.choices[0].message.content

def request3(state: State, prompt: str) -> str:
    """
    Send a prompt to the GPT-3 API and return the response.

    Args:
        - state: The current state of the app.
        - prompt: The prompt to send to the API.

    Returns:
        The response from the API.
    """
    response = state.client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content

def update_context(state: State) -> None:
    """
    Update the context with the user's message and the AI's response.

    Args:
        - state: The current state of the app.
    """
    state.context += f"Human: \n {state.current_user_message}\n\n AI:"
    answer = request3(state, state.context).replace("\n", "")
    state.context += answer

    return answer

def send_message(state: State) -> None:
    """
    Send the user's message to the API and update the context.

    Args:
        - state: The current state of the app.
    """
    notify(state, "info", "Sending to GPT")
    answer = update_context(state)
    conv = state.conversation._dict.copy()
    conv["Conversation"] += [state.current_user_message, answer]
    state.current_user_message = ""
    state.conversation = conv
    notify(state, "success", "Response sent to GPT!")
    
def send_image(state: State) -> None:
    image = Image.open(state.current_image)
    # image.save("src/saved/fixed_img.png")
    # image_resize()

    aPlant = plant_id.Plant_ID()
    pdq = plantDiseaseQuery.plantDiseaseQuery()
    
    identification = aPlant.identify_plant(state.current_image)
    health = aPlant.health_assessment_plant(state.current_image)
    pdq.add_plant(aPlant,identification,health, state.current_image)
    
    state.plants = pdq.get_plant_id_name()

    #  # Add the user's message to the context
    # state.context += f"Human: GPT, your task is to identify the type of plant and identify that plant health issues with precision. If a condition is unrecognizable, reply with \'I don\'t know\'. Analyze any image of a plant or leaf I provide, and detect all abnormal conditions, whether they are diseases, pests, deficiencies, or decay. Respond strictly with the name of the condition identified, and nothing else—no explanations, no additional text. If a condition is unrecognizable, reply with \'I don\'t know\'. If the image is not plant-related, say \'Please pick another image\n ' \n\n AI:"
    
    # # Send the user's message to the API and get the response
    # answer = request4(state, base64_image).replace("\n", "")
    
    # # Add the response to the context for future messages
    # state.context += answer
    # # Update the conversation
    # conv = state.conversation._dict.copy()
    # conv["Conversation"] += ["Based on the image this is my answer:", answer]
    # state.conversation = conv
    
#clear the chat
def clear_history(state: State) -> None:
    state.conversation = {"Conversation": [f"I've just adopted a plant and it's name is {state.plant_name} I would like to know more about it", "Hi! I can take a look at it and tell you about it."]}
    state.context = f"GPT, your task is to tell me more about the health and care of my plant whose name is {state.plant_name}"

#style
def style_conv(state: State, idx: int, row: int) -> str:
    """
    Apply a style to the conversation table depending on the message's author.

    Args:
        - state: The current state of the app.
        - idx: The index of the message in the table.
        - row: The row of the message in the table.

    Returns:
        The style to apply to the message.
    """
    if idx is None:
        return None
    elif idx % 2 == 0:
        return "user_message"
    else:
        return "gpt_message"
    
stylekit = {
  "color_primary": "#BADA55",
  "color_secondary": "#C0FFE",
  
  "color_background_light" : "#F0F5F7",
  "color_background_dark": "#152335",
  
  "font_family" : "Lato, Arial, sans-serif",

}

#plant functions

pdq = plantDiseaseQuery.plantDiseaseQuery()
plants = pdq.get_plant_id_name()
value = None

def UpdateImage(state:State) -> None:
    image_resize()
    pil_img = Image.open("src/saved/fixed_img.png")
    image_bytes = io.BytesIO()
    pil_img.save(image_bytes, format='PNG')
    image = image_bytes.getvalue()
    state.current_image = image

def UpdateDashboard(state:State, plant:dict) -> None:
    # print(plant)
    state.plant_name = plant['plantName']
    state.Common_Name = state.Common_Name = ", ".join([plant['commonName']] if isinstance(plant['commonName'], str) else plant['commonName'])

    state.Healthy = "Sick 😷" if plant['hasDisease'] == False else "Healthy 💪"
    state.Chance = str(plant['probability'])
    state.Disease_Name = plant['diseaseName']
    state.Disease_Description = plant['description']
    state.Chemical_Treatment = plant['chemicalTreatment']
    state.Biological_Treatment = plant['biologicalTreatment']
    state.Prevention = plant['prevention']
    state.context = f"I've adopted a plant named {state.plant_name} it's common name is {state.Common_Name} that is currently {state.Healthy} with chance of diseases {state.Chance}. Can you help me answer a few questions about it?"
    
    conv = state.conversation._dict.copy()
    conv["Conversation"] = [f"I've just adopted a plant and it's name is {state.plant_name}. I would like to know more about it", "Hi! I can take a look at it and tell you about it."]
    state.conversation = conv
    
def getPlantInfo(state : State, var_name : str, value : any) -> None:
    print(value)
    print("A plant has been selected")
    print(value)
    plant = pdq.get_plant_by_id(value[0])
    print(plant.keys())                                   
    pil_img = Image.open(io.BytesIO(plant['image']))
    pil_img.save("src/saved/fixed_img.png")
    UpdateImage(state)
    UpdateDashboard(state,plant)


logo = "src/images/logo.png"
#USER INTERFACE

page = """
<|toggle|theme|>
   
   
<|layout|columns=1 5|

<|sidebar|
<|{logo}|image|width = 255px|>
<br/>
<br/>
<|{current_image}|file_selector|on_action=send_image|extensions=.png,.jpg,.jpeg|label=Add a New Plant|>

<br/>
<br/>
<|{value}|selector|lov={plants}|multiple = False|filter|width = 100%|on_change=getPlantInfo|>
|>

<|part|render=True|class_name=dashboard|
## 🌱 Plant *Dashboard*{: .color-primary}
<|2 1|layout|
<|part|render=True|class_name=plant_info|id = part

<|card card-bg|
**Plant Name:**
<|{plant_name}|>
<br/><br/>
**Common Names:**
<|{Common_Name}|>
<br/><br/>
**Healthy?**
<|{Healthy}|>
<br/><br/>
**Chance of Disease:**
<|{Chance}|>
<br/><br/>
**Disease Name:**
<|{Disease_Name}|>
<br/><br/>
**Disease Description:**
<|{Disease_Description}|>
<br/><br/>
**Chemical Treatment:**
<|{Chemical_Treatment}|>
<br/><br/>
**Biological Treatment:**
<|{Biological_Treatment}|>
<br/><br/>
**Prevention:**
<|{Prevention}|>
<br/>
|>

|>

<|part|render=True|class_name=plant_photo|
<|{current_image}|image|width=100%|>
|>

|>

<br/>
<|part|render=True|class_name=plant_upload align-item-bottom table|
<|{conversation}|table|style=style_conv|show_all|width=100%|height = 200px|rebuild|>
<|{current_user_message}|input|label= Ask GPT here...|on_action=send_message|class_name=fullwidth|>
<|Clear History|button|class_name=clear|on_action=clear_history|>
|>
|>
|>
"""

#To run the application
if __name__ == "__main__":
    Gui(page).run(title="Plant Whisperer", use_reloader=True, stylekit = stylekit, port = 5001)