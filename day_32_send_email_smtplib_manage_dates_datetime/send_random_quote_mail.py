import random
import smtplib
import datetime as dt

EMAIL_PROVIDER = "smtp.gmail.com"
with open("quotes.txt") as file:
    QUOTES = file.readlines()
MY_EMAIL = input("Your Gmail: ")
MY_PASS = input("Your Gmail Password: ")
MAIL_TO_ADDR = "quinnton.jacieon@freedrops.org"

def send_random_quote_mail():

    quote = random.choice(QUOTES).strip()
    email_msg = f"Subject:Quote of the Day\n\nHello, Friend!\n\n{quote}"

    print(f"Sending Mail to: {MAIL_TO_ADDR} ...")
    with smtplib.SMTP(host=EMAIL_PROVIDER, port=587) as connection:  # or port=25
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MAIL_TO_ADDR,
            msg = email_msg
        )
    print("Email Sent!")


if __name__ == "__main__":

    now = dt.datetime.now()
    if now.weekday() == 0:  # Check whether current day is Monday
        send_random_quote_mail()
