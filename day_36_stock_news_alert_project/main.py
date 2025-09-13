"""Day 36. Stock News Monitoring Project"""

import requests
import json
from datetime import datetime, timedelta
import pytz
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_API_KEY = ""
NEWS_API = ""
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE = ""
MY_PHONE = ""

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day
# before yesterday then print("Get News").
# --------------------- TIME_SERIES_DAILY --------------------------------- #
url = "https://www.alphavantage.co/query"
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_API_KEY,
}
resp = requests.get(url, params=params)
resp.raise_for_status()
time_series = resp.json()["Time Series (Daily)"]

time_series_iterator = iter(time_series.values())
yesterday_price = float(next(time_series_iterator)["4. close"])
day_bfr_yesterday_price = float(next(time_series_iterator)["4. close"])

'''     Formula for Percentage Change:
Percentage Change = (Today’s Close − Yesterday’s Close) / Yesterday’s Close × 100

* close — the stock price at the end of the day (often used for tracking overall performance).
'''
stock_change = (yesterday_price - day_bfr_yesterday_price) / \
    day_bfr_yesterday_price * 100

if stock_change > 0:
    stock_change_info = f"🔺{stock_change:.1f}%"
else:
    stock_change_info = f"🔻{stock_change * -1:.1f}%"
print(f"Change of Stock Price: [{STOCK}]", stock_change_info)


# # --------------------- TIME_SERIES_INTRADAY ------------------------------ #
# url = "https://www.alphavantage.co/query"

# params = {
#     "function": "TIME_SERIES_INTRADAY",
#     "interval": "60min",
#     "symbol": STOCK,
#     "apikey": ALPHA_VANTAGE_API_KEY,
# }
# resp = requests.get(url, params=params)
# resp.raise_for_status()
# time_series = resp.json()["Time Series (60min)"]

# # Define local timezone (UTC+5)
# local_tz = pytz.timezone("Asia/Tashkent")
# # Get the cutoff time in local timezone
# cutoff_time = datetime.now(local_tz) - timedelta(hours=48)

# for time_stamp, stock_data in time_series.items():
#     print(time_stamp)
#     print(stock_data, end="\n\n")

#     # Parse the timestamp (naive datetime)
#     ts = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
#     # Convert the US/Eastern time to local timezone (UTC+5)
#     ts_local = ts.astimezone(local_tz)
#     # Compare with the cutoff time (already in local timezone)
#     if ts_local < cutoff_time:
#         break


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for
# the COMPANY_NAME.
url = "https://newsapi.org/v2/everything"
params = {
    "q": COMPANY_NAME,
    "to": "2025-09-12",
    "sortBy": "popularity",
    "apiKey": NEWS_API,
    "language": "en",
}

resp = requests.get(url, params=params)
resp.raise_for_status()

msg_text = f"{STOCK}: {stock_change_info}"
news_count = 1
# print(resp.json()["articles"])
for article in resp.json()["articles"]:
    if COMPANY_NAME.lower() in article["title"].lower() + \
        article["description"].lower() + article["content"].lower():

        msg_text += f"\nHeadline-{news_count}: {article["title"].strip()}\n"
        msg_text += f"Brief-{news_count}: {article["description"].strip()}\n"
        news_count += 1
    if news_count == 4:
        break


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title
# and description to your phone number. 

if abs(stock_change) >= 5:
    print("\n\t<Sending a Message> :")
    print(msg_text)

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        from_=TWILIO_PHONE,
        to=MY_PHONE,
        body=msg_text,
    )
    print("\nMessage Status:", msg.status)
