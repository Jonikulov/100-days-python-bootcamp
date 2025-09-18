import os
from dotenv import load_dotenv
from twilio.rest import Client
from smtplib import SMTP

load_dotenv()

class NotificationManager:
    '''This is responsible for sending notifications with the deal flight details'''

    def __init__(self):
        self._twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self._twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self._twilio_phone = os.getenv("TWILIO_PHONE")
        self._my_phone = os.getenv("MY_PHONE")
        self._my_email = os.getenv("MY_EMAIL")
        self._my_email_pass = os.getenv("GMAIL_APP_PASS")

    def send_sms_msg(self, msg_text):
        client = Client(self._twilio_account_sid, self._twilio_auth_token)
        msg = client.messages.create(
            from_=self._twilio_phone,
            to=self._my_phone,
            body=msg_text,
        )
        print("Message Status:", msg.status, end="\n\n")

    def send_emails(self, emails: list, msg_text: str):
        for mail_to in emails:
            print("Sending email to:", mail_to)
            with SMTP(host="smtp.gmail.com") as conn:  # or port: 587 / 25
                conn.starttls()
                conn.login(user=self._my_email, password=self._my_email_pass)
                conn.sendmail(
                    from_addr = self._my_email,
                    to_addrs = mail_to,
                    msg = msg_text
                )
