import logging

from app import create_app
from dotenv import load_dotenv
import os
import requests


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
print(VERIFY_TOKEN)
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

app = create_app()

if __name__ == "__main__":

    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8001)


