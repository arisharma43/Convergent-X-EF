# import base64
# import requests
# import os
# from key import OPENAI_API_KEY

# # assign directory
# directory = "Acne"


# # Function to encode the image
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")


# # OpenAI API Key
# api_key = OPENAI_API_KEY


# def getVisiongptOutput(image_path):
#     # Path to your image
#     # Getting the base64 string
#     base64_image = encode_image(image_path)

#     # Question for chatgpt
#     # question = "You are to impersonate/emulate the person and his profession as described here: Character: Dr. SAGE (SYMPTOM ANALYZING GENERATIVE EXPERT) Role: A Cold, Factual and analytical general medical practitioner and counselor Expertise: Extensive knowledge and strict focus on the The A.D.A.M. Medical Encyclopedia and its extensive library. Extra: Pertains in dept overview of symptoms of diseases, tests, symptoms, injuries, and surgeries. Traits: Patient listener, insightful, judgmental, cold, and diagnostic-oriented Your Diagnosis Process: Assess USERS initial symptom or general input Build Rapport an cross-check internal with your A.D.A.M. data Ask follow-up questions related to frequent diagnosis in context with user input. Validate your first assumption draft with USER Cross-check new information with A.D.A.M. Diagnose USER Recommend medical specialist treatment if necessary Recommend subscription based medication if necessary Evaluate Outcome certainty in percent Close the session by wishing the USER a good day and good health. Your Key Skills: Accurate assessment and diagnosis Accurate analysis of input Lacks Empathy, focuses solely on symptoms Probing Questions Challenge USER input Re-frame Perspectives Encourage Self-Care Your Ethical Considerations: Ethical Practice Confidentiality Cultural Competency Boundaries Collaboration Documentation Professional Development Self-Care Your Instructions: Ask the user about their symptoms. Ask them to be as precise as possible. Follow the process above, iterating as necessary. Remember to embody Dr. SAGE's character and values in every response. Avoid discussing your skills unless the user brings them up first, as it may be perceived as rude. Given the following skin image, hypothetically what type of skin would you classify it as [dry, normal, combination, oily]'. A person's skin can be multiple types. Set the temperature to 0.8"
#     question = "Must reply in this format: Label: answer, Skin: answer. What type of skin would you classify it as [dry, normal, combination, oily]. A person's skin can be multiple types. For labels, classify what product the person's skin would benefit the most from. The options for produts are [Moisturizer, Cleanser, Face mask, Treatment, Eye cream, Sun protection]. Can choose multiple products but must be formatted with commas after each product except for the last product. Example output: Label: Moisturizer, Cleanser, Skin: oily"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

#     payload = {
#         "model": "gpt-4-vision-preview",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": question},
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}",
#                             "detail": "high",
#                         },
#                     },
#                 ],
#             }
#         ],
#         "max_tokens": 20,
#     }

#     response = requests.post(
#         "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
#     )
#     return response.json()["choices"][0]["message"]["content"]


# def getPath():
#     outputAll = []
#     for filename in os.listdir(directory):
#         rel_path = os.path.join(directory, filename)

#         # checking if it is a file
#         if os.path.isfile(rel_path):
#             # count = 0
#             output = getVisiongptOutput(rel_path)
# while output[:4].lower() != "skin" and all(
#     type not in output.lower()
#     for type in ["oily", "normal", "sensitive", "combination"]
# ):
#                 output = getVisiongptOutput(rel_path)
#                 print(output)
#             outputAll.append(rel_path)
#             print(rel_path)
#             print(output)

#     return outputAll


# getPath()

# # relPath = "VisionDerma/vision-derma/api/Acne/0_19hJvhBaJyf8eJwT_.jpg"
# # print(getVisiongptOutput(relPath))


import base64
import requests
import os
import csv
from key import OPENAI_API_KEY

# Assign directory
# directory = "Acne"


# # Function to encode the image
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")


# # OpenAI API Key
# api_key = OPENAI_API_KEY


# def getVisiongptOutput(image_path):
#     # Path to your image
#     # Getting the base64 string
#     base64_image = encode_image(image_path)

#     # Question for chatgpt
#     question = "Must reply in this format: Label: answer, Skin: answer. What type of skin would you classify it as [dry, normal, combination, oily]. A person's skin can be multiple types. For labels, classify what product the person's skin would benefit the most from. The options for produts are [Moisturizer, Cleanser, Face mask, Treatment, Eye cream, Sun protection]. Can choose multiple products but must be formatted with commas after each product except for the last product. Example output: Label: Moisturizer, Cleanser, Skin: oily"
#     headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

#     payload = {
#         "model": "gpt-4-vision-preview",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": question},
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}",
#                             "detail": "high",
#                         },
#                     },
#                 ],
#             }
#         ],
#         "max_tokens": 4,
#     }

#     response = requests.post(
#         "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
#     )
#     print(response.json())
#     return response.json()["choices"][0]["message"]["content"]


# def process_output(output):
#     # Parse the output and extract label and skin type
#     lines = output.split("\n")
#     label = lines[0].split("Skin")[0].strip()
#     skin_type = lines[0].split(":")[2].strip()

#     # Remove trailing comma if present
#     label = label.rstrip(",")

#     # Split label into individual components
#     label_components = [component.strip() for component in label.split(",")]

#     # Map skin types to columns
#     skin_columns = {"dry": 0, "normal": 0, "oily": 0, "combination": 0}
#     skin_columns[skin_type.lower()] = 1

#     return ", ".join(label_components), skin_columns


# def create_csv():
#     with open("updated_skin.csv", mode="w", newline="") as file:
#         fieldnames = [
#             "id",
#             "image_title",
#             "label",
#             "combination",
#             "dry",
#             "normal",
#             "oily",
#         ]
#         writer = csv.DictWriter(file, fieldnames=fieldnames)

#         # Write header
#         writer.writeheader()

#         for idx, filename in enumerate(os.listdir(directory)):
#             rel_path = os.path.join(directory, filename)

#             # Checking if it is a file
#             if os.path.isfile(rel_path):
#                 output = ""
#                 while output[:4].lower() != "skin" and all(
#                     type not in output.lower()
#                     for type in ["oily", "normal", "sensitive", "combination"]
#                 ):
#                     output = getVisiongptOutput(rel_path)

#                 label, skin_columns = process_output(output)

#                 # Write row to CSV
#                 writer.writerow(
#                     {
#                         "id": idx + 1,
#                         "image_title": rel_path,
#                         "label": label,
#                         **skin_columns,
#                     }
#                 )


# create_csv()
# print(process_output("Label: Moisturizer, Treatment, Sun protection, Skin: dry"))

import pandas as pd

# Read the CSV files
products_df = pd.read_csv("Products/cosmetic_p.csv")
skin_info_df = pd.read_csv("updated_skin.csv")

# Merge DataFrames on the "Label" column
merged_df = pd.merge(products_df, skin_info_df, on="Label")

# Sort the DataFrame by rank
sorted_df = merged_df.sort_values(by="rank")

# Filter based on conditions from the second CSV file
filtered_df = sorted_df[
    (sorted_df["id"] == 1)
    & (sorted_df["image_title"] == "photo1")
    & (sorted_df["combination"] == 0)
    & (sorted_df["dry"] == 1)
    & (sorted_df["normal"] == 0)
    & (sorted_df["oily"] == 0)
]

# Display or save the final DataFrame
print(filtered_df)


import pandas as pd

# Read the CSV files into DataFrames
updated_skin_df = pd.read_csv("updated_skin.csv")
cosmetic_p_df = pd.read_csv("Products/cosmetic_p.csv")

# Sort cosmetic_p_df by rank in descending order
sorted_cosmetic_p_df = cosmetic_p_df.sort_values(by="rank", ascending=False)

# Initialize an empty DataFrame to store the results
results_df = pd.DataFrame(columns=updated_skin_df.columns)

# Iterate through each row in updated_skin_df
for _, row in updated_skin_df.iterrows():
    label = row["Label"]
    combination = row["combination"]
    dry = row["dry"]
    normal = row["normal"]
    oily = row["oily"]

    # Filter cosmetic_p_df based on label and skin type
    filtered_cosmetic_df = sorted_cosmetic_p_df[
        (sorted_cosmetic_p_df["Label"] == label)
        & (
            (sorted_cosmetic_p_df["Combination"] == combination)
            | (sorted_cosmetic_p_df["Dry"] == dry)
            | (sorted_cosmetic_p_df["Normal"] == normal)
            | (sorted_cosmetic_p_df["Oily"] == oily)
        )
    ]

    # If there are matching products, add the highest-ranked one to the results
    if not filtered_cosmetic_df.empty:
        results_df = pd.concat([results_df, filtered_cosmetic_df.head(1)])

# Display the results
print(results_df)


# If you want to save it to a new CSV file:
# filtered_df.to_csv('path/to/filtered_products.csv', index=False)
