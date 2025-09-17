import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
MY_PHONE = os.getenv("MY_PHONE")

class NotificationManager:
    '''This is responsible for sending notifications with the deal flight details'''

    def __init__(self, msg_text):
        self.msg_text = msg_text

    def send_sms_msg(self):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            from_=TWILIO_PHONE,
            to=MY_PHONE,
            body=self.msg_text,
        )
        print("Message Status:", msg.status, end="\n\n")
