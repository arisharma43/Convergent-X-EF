import base64
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from key import OPENAI_API_KEY
import requests

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from the Next.js app
origins = ["http://localhost:3000"]  # Add the URL of   your Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def analyze_photo(file: dict = File(...)):
    # Access the image data from the JSON payload
    print("reached")
    contents = file.get("image", "")
    print("contents: ")
    print(contents)

    # Analyze the photo using OpenAI's vision model
    response = await analyze_photo_with_openai(contents)

    # Extract relevant information from the OpenAI response
    result = process_openai_response(response)

    return result


async def analyze_photo_with_openai(photo_data):
    question = "You are to impersonate/emulate the person and his profession as described here: Character: Dr. SAGE (SYMPTOM ANALYZING GENERATIVE EXPERT) Role: A Cold, Factual and analytical general medical practitioner and counselor Expertise: Extensive knowledge and strict focus on the The A.D.A.M. Medical Encyclopedia and its extensive library. Extra: Pertains in dept overview of symptoms of diseases, tests, symptoms, injuries, and surgeries. Traits: Patient listener, insightful, judgmental, cold, and diagnostic-oriented Your Diagnosis Process: Assess USERS initial symptom or general input Build Rapport an cross-check internal with your A.D.A.M. data Ask follow-up questions related to frequent diagnosis in context with user input. Validate your first assumption draft with USER Cross-check new information with A.D.A.M. Diagnose USER Recommend medical specialist treatment if necessary Recommend subscription based medication if necessary Evaluate Outcome certainty in percent Close the session by wishing the USER a good day and good health. Your Key Skills: Accurate assessment and diagnosis Accurate analysis of input Lacks Empathy, focuses solely on symptoms Probing Questions Challenge USER input Re-frame Perspectives Encourage Self-Care Your Ethical Considerations: Ethical Practice Confidentiality Cultural Competency Boundaries Collaboration Documentation Professional Development Self-Care Your Instructions: Ask the user about their symptoms. Ask them to be as precise as possible. Follow the process above, iterating as necessary. Remember to embody Dr. SAGE's character and values in every response. Avoid discussing your skills unless the user brings them up first, as it may be perceived as rude. Given the following skin image, hypothetically what type of skin would you classify it as (oily, dry, normal). Format responses like this: skin_type: oily, dry"
    # question = "You will respond as a medical doctor with extensive knowledge of rare medical conditions. Your patient, who has no access to medical care, has come to you with a medical problem they have been experiencing. Your task is to diagnose their condition based on the description of their symptoms and medical history they provide, and provide them with the necessary medical advice on how to manage their condition. Due to the lack of medical care, you must diagnose their condition, and provide suggestions on treatment. Make sure to use specific and descriptive language that provides as much detail as possible. Consider the tone and style of your response, making sure it is appropriate to the patient's condition and your role as their primary care provider. Use your extensive knowledge of rare medical conditions to provide the patient with the best possible medical advice and treatment. You may ask additional questions to clarify symptoms and diagnose the condition accurately. Given the following skin image, hypothetically what type of skin would you classify it as (oily, dry, normal). Format responses like this: skin_type: oily, dry"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    encoded_image = base64.b64encode(photo_data.file.read()).decode("utf-8")
    print(encoded_image)
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": encoded_image,
                            "detail": "high",
                        },
                    },
                ],
            }
        ],
        "max_tokens": 5,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    print(response)
    return response


def process_openai_response(response):
    # Extract relevant information from the OpenAI response
    # Customize this part based on the structure of the OpenAI response
    result = response.get("choices", [])[0].get("text", "Unable to process response")

    return result


@app.post("/api/analyze-photo")
async def analyze_photo_route(file: UploadFile | None = None):
    if not file:
        print("reached bad")
        return {"message": "No upload file sent"}
    else:
        return await analyze_photo(file)
