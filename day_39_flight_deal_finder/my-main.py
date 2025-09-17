"""Day 39. Capstone Part 1: Flight Deal Finder"""

'''     Program Requirements:
* [x] Use the Flight Search and Sheety API to populate your own copy of the Google
Sheet with International Air Transport Association (IATA) codes for each city.
Most of the cities in the sheet include multiple airports, you want the city
code (not the airport code see here).

* [x] Use the Flight Search API to check for the cheapest flights from tomorrow to
6 months later for all the cities in the Google Sheet.

* [x] If the price is lower than the lowest price listed in the Google Sheet then
send an SMS (or WhatsApp Message) to your own number using the Twilio API.

* [x] The SMS should include the departure airport IATA code, destination airport
IATA code, flight price and flight dates.'''

import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client
from datetime import date, timedelta

load_dotenv("../.env")

AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")
SHEETY_USERNAME = os.getenv("SHEETY_USERNAME")
SHEETY_AUTH_TOKEN = os.getenv("SHEETY_AUTH_TOKEN")
SHEETY_PROJECT_NAME = "flightDeals"
SHEETY_SHEET_NAME = "prices"
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
MY_PHONE = os.getenv("MY_PHONE")
SHEETY_API_URL = f"https://api.sheety.co/{SHEETY_USERNAME}/" \
    f"{SHEETY_PROJECT_NAME}/{SHEETY_SHEET_NAME}"

def get_amadeus_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_CLIENT_ID,
        "client_secret": AMADEUS_API_SECRET,
    }
    resp = requests.post(url, headers=header, data=payload)
    return resp.json()["access_token"]

AMADEUS_ACCESS_TOKEN = get_amadeus_access_token()

def get_sheet_rows() -> list:
    header = {"Authorization": f"Bearer {SHEETY_AUTH_TOKEN}"}
    resp = requests.get(SHEETY_API_URL, headers=header)
    resp.raise_for_status()
    return resp.json()["prices"]


def get_city_iata_code(city_name: str) -> str:
    url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
    header = {"Authorization": f"Bearer {AMADEUS_ACCESS_TOKEN}"}
    params = {"keyword": city_name, "max": 1}
    resp = requests.get(url, params=params, headers=header)
    resp.raise_for_status()
    city_iata_code = resp.json()["data"][0]["iataCode"]
    return city_iata_code


def put_iata_code(city_iata_code: str, row_id: int) -> int:
    header = {"Authorization": f"Bearer {SHEETY_AUTH_TOKEN}"}
    payload = {"price": {"iataCode": city_iata_code}}
    resp = requests.put(
        SHEETY_API_URL + f"/{row_id}",
        headers=header,
        json=payload
    )
    resp.raise_for_status()
    return resp.status_code


def search_flight(
        loc_code: str,
        dest_code: str,
        departure_date: str,
        max_price: int,
        adults: int = 1,
        currency_code: str = "USD",
        ) -> dict:
    print("\tChecking flight price:", departure_date)
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    header = {"Authorization": f"Bearer {AMADEUS_ACCESS_TOKEN}"}
    params = {
        "departureDate": departure_date,  # YYYY-MM-DD
        "originLocationCode": loc_code,
        # city/airport IATA code
        "destinationLocationCode": dest_code,
        "adults": adults,
        "maxPrice": max_price,
        "currencyCode": currency_code,
        "max": 2,
    }
    resp = requests.get(url, params=params, headers=header)
    resp.raise_for_status()
    resp_json = resp.json()
    if resp_json["meta"]["count"] > 0:
        return resp_json["data"][0]
    return dict()


def send_sms_msg(msg_text):
    print(f"\n\t<Sending SMS...> :\n{msg_text}\n")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        from_=TWILIO_PHONE,
        to=MY_PHONE,
        body=msg_text,
    )
    print("\nMessage Status:", msg.status)


def main():
    # Get IATA code for each city
    fly_from = input("Enter your current location city name: ")
    fly_from = get_city_iata_code(fly_from)
    for row in get_sheet_rows():
        print(
            f"{row['id']}. Retrieving IATA code: {row["city"]} -- ",
            flush=True,
            end=""
        )
        # Retrieve proper city IATA code
        iata_code = get_city_iata_code(row["city"])
        print(iata_code)

        # Update the sheet by filling IATA code of the city
        put_iata_code(iata_code, row["id"])

        # Get flight data
        tomorrow = date.today() + timedelta(days=1)
        date_from = date.strftime(tomorrow, "%Y-%m-%d")
        for day in range(1, 5):  # TODO: 181
            depart_date = date.strftime(date.today() + timedelta(days=day), "%Y-%m-%d")
            # Check the current flight price
            flight_offer = search_flight(fly_from, iata_code, depart_date, row["lowestPrice"])
            if flight_offer:
                new_price = float(flight_offer["price"]["total"])
                if new_price < row["lowestPrice"]:
                    flight_offer["lastTicketingDate"]
                    # If lower price available then send SMS
                    message = f"Low price alert! Only ${new_price} to fly " \
                        f"from {fly_from} to {iata_code}, on {date_from} " \
                        f"until {depart_date}."
                    send_sms_msg(message)
                    break


if __name__ == "__main__":
    main()
