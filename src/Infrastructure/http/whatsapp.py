import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
TWILIO_CONTENT_SID = os.getenv("TWILIO_CONTENT_SID")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number: str, code: str):
    try:
        message = client.messages.create(
        from_=F'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
        content_sid=TWILIO_CONTENT_SID,
        content_variables=f'{{"1":"{code}"}}',
        to=f'whatsapp:{to_number}'
        )

        return message.sid
    except Exception as e:
        raise e
