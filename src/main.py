#imports
from taipy.gui import Gui, State, notify
import taipy.gui.builder as tgb
import openai
from PIL import Image
from io import BytesIO
import base64

#initialize variables

#context for gpt
context = ""

# initialised dictionary storing the conversation history
conversation = {
    "Conversation": ["I've just adopted a plant", "Hi! I can take a look at it and tell you about it."]
}

#message that user will type
current_image = ""

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
    image.save("saved/fixed_img.png")
    
    with open(state.current_image, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
     # Add the user's message to the context
    state.context += f"Human: GPT, your task is to identify the type of plant and identify that plant health issues with precision. If a condition is unrecognizable, reply with \'I don\'t know\'. Analyze any image of a plant or leaf I provide, and detect all abnormal conditions, whether they are diseases, pests, deficiencies, or decay. Respond strictly with the name of the condition identified, and nothing else—no explanations, no additional text. If a condition is unrecognizable, reply with \'I don\'t know\'. If the image is not plant-related, say \'Please pick another image\n ' \n\n AI:"
    image.show()
    
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
  
  "font_family" : "Lato, Arial, sans-serif"
}
#USER INTERFACE

page = """
<|toggle|theme|>
   
   
<|layout|columns=450px 1|
<|part|render=True|class_name=sidebar|
|>

<|part|render=True|class_name=p2|
## Plant **Dashboard**
<|card| 400px 1|
**Dashboard2**
<|part|render=True|class_name=conversation|
<|{conversation}|table|style=style_conv|show_all|width=100%|rebuild|>
<|{current_image}|file_selector|label=Add the image of plant here|on_action=send_image|extensions=.png,.jpg,.jpeg|class_name=fullwidth|>
<|Clear History|button|class_name=clear|on_action=clear_history|>
|>
|>
|>
|>
"""

#To run the application
if __name__ == "__main__":
    Gui(page).run(title="Taipy Chat", use_reloader=True, stylekit = stylekit)
    