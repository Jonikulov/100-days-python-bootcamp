"""Day 38. Workout Tracking Using Google Sheets"""

import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv("../.env")

NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")
SHEETY_USERNAME = os.getenv("SHEETY_USERNAME")
SHEETY_PROJECT_NAME = os.getenv("SHEETY_PROJECT_NAME")
SHEETY_SHEET_NAME = os.getenv("SHEETY_SHEET_NAME")
SHEETY_AUTH_TOKEN = os.getenv("SHEETY_AUTH_TOKEN")
SHEETY_API_URL = f"https://api.sheety.co/{SHEETY_USERNAME}/" \
    f"{SHEETY_PROJECT_NAME}/{SHEETY_SHEET_NAME}"

host_domain = "https://trackapi.nutritionix.com"
nl_exercise_endpoint = "/v2/natural/exercise"
exercise_query = input("Exercise Query: ")
headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
}
payload = {
    "query": exercise_query,
    "weight_kg": 50,
    "height_cm": 172,
    "age": 22,
}

resp = requests.post(
    host_domain + nl_exercise_endpoint,
    headers=headers,
    json=payload,
)
resp.raise_for_status()
exercises = resp.json()["exercises"]


header = {"Authorization": f"Bearer {SHEETY_AUTH_TOKEN}"}
now = datetime.now()
for exercise in exercises:
    payload = {
        "sheet1": {
            "date": datetime.strftime(now, "%d/%m/%Y"),
            "time": datetime.strftime(now, "%H:%M:%S"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
    }}

    resp = requests.post(SHEETY_API_URL, headers=header, json=payload)
    resp.raise_for_status()
    print(resp)
    print(resp.text)

