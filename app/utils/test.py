import requests
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
print(VERIFY_TOKEN)
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

phone_number_id = "your-phone-number-ID"
access_token = ACCESS_TOKEN
url = f'https://graph.facebook.com/v13.0/181790545019298/message_qrdls'
params = {
    'prefilled_message': 'Embarquez à bord du navire !',
    'generate_qr_image': 'PNG',
    'access_token': access_token
}

response = requests.post(url, params=params)

# Afficher la réponse
print(response.text)
