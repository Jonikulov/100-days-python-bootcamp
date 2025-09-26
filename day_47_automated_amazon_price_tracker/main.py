"""Day 47. Automated Amazon Price Tracker"""

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from smtplib import SMTP
from email.mime.text import MIMEText

load_dotenv()
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASS = os.getenv("GMAIL_APP_PASS")
EMAIL_PROVIDER_HOST = "smtp.gmail.com"

BUY_PRICE = 100

def send_email_alert(message):
    # Wrap message in MIMEText with UTF-8 encoding
    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = "Amazon Price Alert!"
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL

    with SMTP(host=EMAIL_PROVIDER_HOST) as conn:  # port: 587 / 25
        conn.starttls()
        conn.login(MY_EMAIL, MY_PASS)
        conn.send_message(msg)


practice_url = "https://appbrewery.github.io/instant_pot"
live_url = "https://amazon.com/dp/B075CYMYK6"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 " \
        "Safari/537.36",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Accept-Language": "en-US",
}
resp = requests.get(live_url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")
# practice website price -> "#size_name_0_price > p"
price = float(soup.select_one(
    "#tp_price_block_total_price_ww > span.a-offscreen").get_text(
        strip=True).split("$")[-1]
)

product_name = soup.select_one("#productTitle").get_text(strip=True)
print("Price:", price)

if price < BUY_PRICE:
    print("Sending price alert email...")
    message = f"Product: {product_name}\nPrice: {price}\nLink: {live_url}"
    send_email_alert(message)
