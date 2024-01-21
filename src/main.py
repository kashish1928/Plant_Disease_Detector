#imports
from taipy.gui import Gui, State, notify
import taipy.gui.builder as tgb
import openai
from PIL import Image
import io
import base64
import plantDiseaseQuery
import matplotlib.pyplot as plt

#initialize variables


#context for gpt
context = ""

#Plant Dashboard vars
plant_name = ""
Common_Name = ""
Healthy = ""
Chance = ""

# initialised dictionary storing the conversation history
conversation = {
    "Conversation": ["I've just adopted a plant", "Hi! I can take a look at it and tell you about it."]
}

current_image = "src/saved/fixed_img.png"

#message that user will type
def image_resize():
    current_image = "src/saved/fixed_img.png"
    image = Image.open(current_image)
    new_image = image.resize((1000, 1000))
    new_image.save(current_image)

image_resize()
#api call
client = openai.Client(api_key="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")


#functions

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

    
    
def send_image(state: State) -> None:
    image = Image.open(state.current_image)
    image.save("src/saved/fixed_img.png")
    image_resize()

    with open(state.current_image, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
     # Add the user's message to the context
    state.context += f"Human: GPT, your task is to identify the type of plant and identify that plant health issues with precision. If a condition is unrecognizable, reply with \'I don\'t know\'. Analyze any image of a plant or leaf I provide, and detect all abnormal conditions, whether they are diseases, pests, deficiencies, or decay. Respond strictly with the name of the condition identified, and nothing else—no explanations, no additional text. If a condition is unrecognizable, reply with \'I don\'t know\'. If the image is not plant-related, say \'Please pick another image\n ' \n\n AI:"
    
    # Send the user's message to the API and get the response
    answer = request4(state, base64_image).replace("\n", "")
    
    # Add the response to the context for future messages
    state.context += answer
    # Update the conversation
    conv = state.conversation._dict.copy()
    conv["Conversation"] += ["Based on the image this is my answer:", answer]
    state.conversation = conv
    

def clear_history(state: State) -> None:
    state.conversation = {"Conversation": []}
    state.context = "GPT, your task is to identify the type of plant and identify that plant health issues with precision. If a condition is unrecognizable, reply with \'I don\'t know\'. Analyze any image of a plant or leaf I provide, and detect all abnormal conditions, whether they are diseases, pests, deficiencies, or decay. Respond strictly with the name of the condition identified, and nothing else—no explanations, no additional text. If a condition is unrecognizable, reply with \'I don\'t know\'. If the image is not plant-related, say \'Please pick another image\""

stylekit = {
  "color_primary": "#BADA55",
  "color_secondary": "#C0FFE",
  
  "color_background_light" : "#F0F5F7",
  "color_background_dark": "#152335",
  
  "font_family" : "Lato, Arial, sans-serif",

}

pdq = plantDiseaseQuery.plantDiseaseQuery()
plants = pdq.get_plant_id_name()
value = None

def UpdateImage(state:State) -> None:
    image_resize()
    pil_img = Image.open("src/saved/fixed_img.png")
    image_bytes = io.BytesIO()
    pil_img.save(image_bytes, format='JPEG')
    image = image_bytes.getvalue()
    state.current_image = image

def UpdateDashboard(state:State, plant:dict) -> None:
    # print(plant)
    state.plant_name = plant['plantName']
    state.Common_Name = state.Common_Name = ", ".join([plant['commonName']] if isinstance(plant['commonName'], str) else plant['commonName'])

    state.Healthy = "Sick 😷" if plant['hasDisease'] == False else "Healthy 💪"
    state.Chance = str(plant['probability'])

def getPlantInfo(state : State, var_name : str, value : any) -> None:
    print("A plant has been selected")
    print(value)
    plant = pdq.get_plant_by_id(value[0][0])
    pil_img = Image.open(io.BytesIO(plant['image']))
    pil_img.save("src/saved/fixed_img.png")
    UpdateImage(state)
    UpdateDashboard(state,plant)
    


logo = "images/logo.png"
#USER INTERFACE

page = """
<|toggle|theme|>
   
   
<|layout|columns=350px 1|

<|sidebar|align-item-center|
<|{logo}|image|width = 275px|>
<br/>
<br/>

<br/>
<br/>
<|{value}|selector|lov={plants}|multiple|filter|width = 400|on_change=getPlantInfo|>
|>

<|part|render=True|class_name=dashboard|
## 🌱 Plant *Dashboard*{: .color-primary}
<|2 1|layout|margin=0.5rem
<|part|render=True|class_name=plant_info|
<|card card-bg|
Plant Name:
<|{plant_name}|>
<br/>
Common Names:
<|{Common_Name}|>
<br/>
Healthy?
<|{Healthy}|>
<br/>
Chance of Disease:
<|{Chance}|>
|>

|>

<|part|render=True|class_name=plant_photo|
<|{current_image}|image|width=100%|>
|>
|>
<|part|render=True|class_name=plant_info|
<|{conversation}|table|style=style_conv|show_all|height=1000px|width=100%|rebuild|>
|>


<|part|render=True|class_name=plant_upload align-item-bottom table|
<|{conversation}|table|style=style_conv|show_all|width=100%|rebuild|>
<|{current_image}|file_selector|on_action=send_image|extensions=.png,.jpg,.jpeg|label=Add the image of plant here|>
<|Clear History|button|class_name=clear|on_action=clear_history|>
|>
|>
|>
"""

#To run the application
if __name__ == "__main__":
    Gui(page).run(title="Plant Whisperer", use_reloader=True, stylekit = stylekit, port = 5001)