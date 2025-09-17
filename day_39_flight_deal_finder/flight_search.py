import os
from dotenv import load_dotenv
import requests

load_dotenv()

class FlightSearch:
    '''This is responsible for talking to the Flight Search API'''
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_CLIENT_ID")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self._api_host = "https://test.api.amadeus.com"
        self._token = self.get_access_token()

    def get_access_token(self):
        url = f"{self._api_host}/v1/security/oauth2/token"
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        resp = requests.post(url, headers=header, data=payload)
        return resp.json()["access_token"]

    def get_city_iata_code(self, city_name: str) -> str:
        url = f"{self._api_host}/v1/reference-data/locations/cities"
        header = {"Authorization": f"Bearer {self._token}"}
        params = {"keyword": city_name, "max": 1}
        resp = requests.get(url, params=params, headers=header)
        try:
            city_iata_code = resp.json()["data"][0]["iataCode"]
        except (KeyError, IndexError):
            print(f"Key/Index Error: No city code found for {city_name}.")
            return "N/A"
        return city_iata_code

    def find_flights(
            self, loc_code: str, dest_code: str, departure_date: str,
            return_date: str, currency_code: str = "USD") -> dict:
        url = f"{self._api_host}/v2/shopping/flight-offers"
        header = {"Authorization": f"Bearer {self._token}"}
        params = {
            "originLocationCode": loc_code,
            "destinationLocationCode": dest_code,
            "departureDate": departure_date,
            "returnDate": return_date,
            "currencyCode": currency_code,
            "adults": 1,
            "max": 5,
            "nonStop": "true",
        }
        resp = requests.get(url, headers=header, params=params)
        return resp.json()
