import os
from dotenv import load_dotenv
import requests

load_dotenv()

class DataManager:
    '''This is responsible for talking to the Google Sheet'''

    def __init__(self):
        self._username = os.getenv("SHEETY_USERNAME")
        self._sheety_api_url = f"https://api.sheety.co/{self._username}/flightDeals"
        self._sheety_auth_token = os.getenv("SHEETY_AUTH_TOKEN")
        self._auth_header = {
            "Authorization": f"Bearer {self._sheety_auth_token}"
        }
        # self.sheet_data = {}

    def get_prices_rows(self) -> list:
        resp = requests.get(self._sheety_api_url + "/prices", headers=self._auth_header)
        return resp.json()["prices"]

    def update_price_row(self, row_id: int, content: dict) -> int:
        url = f"{self._sheety_api_url + "/prices"}/{row_id}"
        payload = {"price": content}
        resp = requests.put(url, headers=self._auth_header, json=payload)
        return resp.status_code

    def get_customer_emails(self) -> list:
        resp = requests.get(self._sheety_api_url + "/users", headers=self._auth_header)
        return resp.json()["users"]
