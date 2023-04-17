import requests
import os
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv

today = datetime.now()
formatted_date = today.strftime("%d/%m/%Y")
formatted_time = today.strftime("%H:%M:%S")

load_dotenv(".env")
NUTRITION_API_KEY = os.getenv('NUTRITION_API_KEY')
NUTRITION_APP_ID = os.getenv('NUTRITION_APP_ID')
SHEETY_ENDPOINT = os.getenv('SHEETY_ENDPOINT')
SHEETY_USERNAME = os.getenv('SHEETY_USERNAME')
SHEETY_PASSWORD = os.getenv('SHEETY_PASSWORD')


GOOGLE_SHEET_NAME = "workout"
GENDER = "male"
WEIGHT_KG = 100
HEIGHT_CM = 187
AGE = 30

nutrition_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-key": NUTRITION_API_KEY,
    "x-app-id": NUTRITION_APP_ID,
}

user_input = input("Tell me what exercises you did: ")

nutrition_config = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

nutrition_response = requests.post(url=nutrition_endpoint, json=nutrition_config, headers=headers)
result = nutrition_response.json()
exercises_data_list = result["exercises"]

for exercise in exercises_data_list:
    sheet_inputs = {
        GOOGLE_SHEET_NAME: {
            "date": formatted_date,
            "time": formatted_time,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }

    sheet_response = requests.post(
        url=SHEETY_ENDPOINT,
        json=sheet_inputs,
        auth=(
            SHEETY_USERNAME,
            SHEETY_PASSWORD,
        )
    )

    print(f"Sheety response:\n {sheet_response.text}")
