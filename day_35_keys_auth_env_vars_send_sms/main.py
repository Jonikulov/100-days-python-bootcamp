"""Day 35. Keys, Authentication, Environment Variables. Send SMS"""

import requests
from twilio.rest import Client

LATITUDE = float()
LONGITUDE = float()
OWM_API_KEY = ""
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
MY_PHONE = ""

def determine_weather_forecast() -> bool:
    owm_endpoint_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": LATITUDE, "lon": LONGITUDE, "cnt": 7, "appid": OWM_API_KEY
    }
    print("Fetching weather data...")
    resp = requests.get(owm_endpoint_url, params=params)
    resp.raise_for_status()
    weather_data = resp.json()
    print("Identifying whether there's any precipitation(s)...")
    for data_step in weather_data["list"]:
        for condition in data_step["weather"]:
            if int(condition["id"]) < 700:
                return True
    return False


def send_sms_msg(message):
    print("Sending SMS message:", message)
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        from_="+18777814538",
        to=MY_PHONE,
        body="Don't forget to get an ☂️ (umbrella)!",
    )
    print("Message Status:", msg.status)


def send_telegram_msg(message):
    # TODO
    pass


if __name__ == "__main__":
    get_umbrella = determine_weather_forecast()
    if get_umbrella:
        message = "Get an umbrella!"
        send_sms_msg(message)
        # OR
        # send_telegram_msg(message)
    else:
        print("No need for umbrella.")
