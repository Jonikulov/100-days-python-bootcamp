"""Day 32. Send Email (smtplib) & Manage Dates (datetime)"""

import pandas as pd
import datetime as dt
import random
import smtplib

EMAIL_PROVIDER = "smtp.gmail.com"
MY_EMAIL = input("Your Email: ")
MY_PASS = input("Your Email Password: ")

# Read birthdays.csv
birthdays_data = pd.read_csv("birthdays.csv")
now = dt.datetime.now()
# Check if any birthday matches with today's date
for _, row in birthdays_data.iterrows():
    today = (now.month, now.day)
    birthday = (int(row["month"]), int(row["day"]))
    if today != birthday:
        continue

    # Send to that person's email a happy birthday mail
    print(f"\nSending Mail to: {row["name"]} ({row["email"]}) ...")
    letter_file = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(letter_file) as file:
        happy_birthday_msg = file.read()
    happy_birthday_msg = f"Subject:Happy Birthday!\n\n{happy_birthday_msg}"

    with smtplib.SMTP(host=EMAIL_PROVIDER, port=587) as conn:  # or port=25
        conn.starttls()
        conn.login(user=MY_EMAIL, password=MY_PASS)
        conn.sendmail(
            from_addr = MY_EMAIL,
            to_addrs = row["email"],
            msg = happy_birthday_msg.replace("[NAME]", row["name"])
        )
    print("Email Sent!")
