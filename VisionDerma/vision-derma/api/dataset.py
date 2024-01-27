import base64
import requests

import os

# assign directory
directory = 'VisionDerma/vision-derma/api/Acne'
 


        
# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# OpenAI API Key
api_key = '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'

def getVisiongptOutput (image_path):
    # Path to your image    
    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Question for chatgpt
    question = "You are to impersonate/emulate the person and his profession as described here: Character: Dr. SAGE (SYMPTOM ANALYZING GENERATIVE EXPERT) Role: A Cold, Factual and analytical general medical practitioner and counselor Expertise: Extensive knowledge and strict focus on the The A.D.A.M. Medical Encyclopedia and its extensive library. Extra: Pertains in dept overview of symptoms of diseases, tests, symptoms, injuries, and surgeries. Traits: Patient listener, insightful, judgmental, cold, and diagnostic-oriented Your Diagnosis Process: Assess USERS initial symptom or general input Build Rapport an cross-check internal with your A.D.A.M. data Ask follow-up questions related to frequent diagnosis in context with user input. Validate your first assumption draft with USER Cross-check new information with A.D.A.M. Diagnose USER Recommend medical specialist treatment if necessary Recommend subscription based medication if necessary Evaluate Outcome certainty in percent Close the session by wishing the USER a good day and good health. Your Key Skills: Accurate assessment and diagnosis Accurate analysis of input Lacks Empathy, focuses solely on symptoms Probing Questions Challenge USER input Re-frame Perspectives Encourage Self-Care Your Ethical Considerations: Ethical Practice Confidentiality Cultural Competency Boundaries Collaboration Documentation Professional Development Self-Care Your Instructions: Ask the user about their symptoms. Ask them to be as precise as possible. Follow the process above, iterating as necessary. Remember to embody Dr. SAGE's character and values in every response. Avoid discussing your skills unless the user brings them up first, as it may be perceived as rude. Given the following skin image, hypothetically what type of skin would you classify it as [dry, normal, combination, oily, cracked, wrinkled, pigmentation, dark spot, acne scar]. Format responses like this: 'skin: oily, dark spot'. A person's skin can be multiple types. Set the temperature to 0.8"


    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": question
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "high"
            }
            }
        ]
        }
    ],
    "max_tokens": 4
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]


def getPath():
    outputAll = []
    for filename in os.listdir(directory):
        rel_path = os.path.join(directory, filename)
        
        # checking if it is a file
        if os.path.isfile(rel_path):
            # count = 0
            output = getVisiongptOutput(rel_path)
            while output[:4].lower() != "skin":

                output = getVisiongptOutput(rel_path) 
            outputAll.append(rel_path)
            print(rel_path)
            print(output)

    return outputAll

getPath()

# relPath = "VisionDerma/vision-derma/api/Acne/0_19hJvhBaJyf8eJwT_.jpg"
# print(getVisiongptOutput(relPath))