from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from key import OPENAI_API_KEY
import httpx

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from the Next.js app
origins = ["http://localhost:3000"]  # Add the URL of your Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def analyze_photo(file: UploadFile = File(...)):
    # Read the contents of the uploaded file
    contents = await file.read()

    # Analyze the photo using OpenAI's vision model
    response = await analyze_photo_with_openai(contents)

    # Extract relevant information from the OpenAI response
    result = process_openai_response(response)

    return result

async def analyze_photo_with_openai(photo_data: bytes):
    # OpenAI Vision API endpoint
    openai_vision_api = "https://api.openai.com/v1/vision/models/your_model_id/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    data = {
        "model": "your_model_id",  # Replace 'your_model_id' with your OpenAI vision model ID
        "prompt": "Analyze the contents of the photo and provide a description.",
        "inputs": {
            "photo": photo_data.decode("utf-8"),
        },
        "max_tokens": 100,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(openai_vision_api, json=data, headers=headers)

    return response.json()

def process_openai_response(response):
    # Extract relevant information from the OpenAI response
    # Customize this part based on the structure of the OpenAI response
    result = response.get("choices", [])[0].get("text", "Unable to process response")

    return result

@app.post('/api/analyze-photo')
async def analyze_photo_route(file: UploadFile = File(...)):
    return await analyze_photo(file)
