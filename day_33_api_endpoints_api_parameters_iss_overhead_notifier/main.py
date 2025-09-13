"""Day 33. API Endpoints & API Parameters. ISS Overhead Notifier"""

''' TASK:
If the ISS is close to my current position (+5/-5)
and it is currently dark
then send me an email to tell me to look up.
Run the code every 60 seconds.
----------------
* Identify & Set your latitude, longitude, time zone, email.
* EVERY 60 SECONDS:
    * Get the ISS location && compare it with mine.
    * If position differences are in [-5, +5] range && \
      if it is dark (time in [from sunset, to sunrise] range) in my time zone:
        * Send email to look telling to look up.
* Functions: iss_overhead, iss_night, send_email.'''

import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from smtplib import SMTP
import time

LATITUDE = float()
LONGITUDE = float()
TIME_ZONE = "Asia/Tashkent"
EMAIL_PROVIDER_HOST = "smtp.gmail.com"
MY_EMAIL = ""
MY_PASS = ""

def iss_overhead() -> bool:
    # Identify ISS location
    print("Sending request to identify ISS location...")
    url = "http://api.open-notify.org/iss-now.json"
    resp = requests.get(url)
    resp.raise_for_status()
    iss_location = resp.json()["iss_position"]
    # Get ISS coordinates
    iss_lat = float(iss_location["latitude"])
    iss_lng = float(iss_location["longitude"])
    # Check whether ISS is near
    if abs(LATITUDE - iss_lat) <= 5 and abs(LONGITUDE - iss_lng) <= 5:
        return True
    return False


def is_night() -> bool:
    # Identify whether it's dark in current time
    print("Sending request to get sunrise & sunset data...")
    url = "https://api.sunrise-sunset.org/json"
    params = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 0,
        "tzid": TIME_ZONE,
    }
    resp = requests.get(url, params=params)
    data = resp.json()["results"]
    resp.raise_for_status()
    # Get sunrise & sunset times
    sunrise = datetime.strptime(data["sunrise"], "%Y-%m-%dT%H:%M:%S%z")
    sunset = datetime.strptime(data["sunset"], "%Y-%m-%dT%H:%M:%S%z")
    now = datetime.now(ZoneInfo(TIME_ZONE))
    # Check whether it's night time
    if sunset <= now <= sunrise:
        return True
    return False


def send_iss_near_email():
    with SMTP(host=EMAIL_PROVIDER_HOST) as conn:  # or port: 587 / 25
        conn.starttls()
        conn.login(user=MY_EMAIL, password=MY_PASS)
        conn.sendmail(
            from_addr = MY_EMAIL,
            to_addrs = MY_EMAIL,
            msg = f"Subject:Look Up!\n\nThe ISS is above you in the sky!"
        )
    print("Sent email to:", MY_EMAIL)


if __name__ == "__main__":

    while True:
        if iss_overhead() and is_night():
            print("ISS is near! Email is being sent...")
            send_iss_near_email()
        else:
            print(
                datetime.strftime(datetime.now(), "%H:%M:%S, %Y-%m-%d --"),
                "ISS is not near and/or it's not dark in current time."
            )
        print()
        # Check every minute
        time.sleep(60)
