import logging
import json

from flask import Blueprint, request, jsonify, current_app

import perso.Bot as Boti
import perso.Allo as Allo
import time

from .decorators.security import signature_required
from .utils.whatsapp_utils import (
    process_whatsapp_message,
    is_valid_whatsapp_message,
)

webhook_blueprint = Blueprint("webhook", __name__)

#Fonctionnement Bot
Bot = Boti.Bot()
TAXI = Allo.Allo(1,"TAXI", False,8,"Vroum vroum")
WRAP_JAMBON = Allo.Allo(2,"WRAP JAMBON", False , 50,"Miam miam")
WRAP_THON = Allo.Allo(4,"WRAP THON", False, 50,"Miam miam")
CHICHA = Allo.Allo(3,"CHICHA", False, 3,"Pff pff")
CREPE = Allo.Allo(4,"CREPE", False,50,"Slap slap")
PANCAKE = Allo.Allo(5,"PANCAKE", False,50,"Pan Pan")
GAUFRE = Allo.Allo(6,"GAUFRE", False,30,"Pou pou")
PATES_CREME_FROMAGE = Allo.Allo(7,"PATES CREME FROMAGE", False,70,"Pou pou")
PATES_ARRABIATA_JAMBON = Allo.Allo(7,"PATES ARRABIATA JAMBON", False,70,"Pou pou")
PETIT_DEJ = Allo.Allo(8,"PETIT DEJ", False,70,"burpp")
PATES_VEGE_CHAMPIGNONS =Allo.Allo(9,"PATES VEGE CHAMPIGNONS", False,70,"burpp")

Bot.addAllo([TAXI, WRAP_THON, WRAP_JAMBON, CHICHA, CREPE, PANCAKE, GAUFRE, PATES_CREME_FROMAGE, PATES_ARRABIATA_JAMBON, PETIT_DEJ, PATES_VEGE_CHAMPIGNONS])

def handle_message(Bot):
    """
    Handle incoming webhook events from the WhatsApp API.

    This function processes incoming WhatsApp messages and other events,
    such as delivery statuses. If the event is a valid message, it gets
    processed. If the incoming payload is not a recognized WhatsApp event,
    an error is returned.

    Every message send will trigger 4 HTTP requests to your webhook: message, sent, delivered, read.

    Returns:
        response: A tuple containing a JSON response and an HTTP status code.
    """
    body = request.get_json()
    # logging.info(f"request body: {body}")

    # Check if it's a WhatsApp status update
    if (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("statuses")
    ):
        logging.info("Received a WhatsApp status update.")
        return jsonify({"status": "ok"}), 200

    try:
        if is_valid_whatsapp_message(body):
            Bot.addMsg(body)
            time.sleep(0.4)
            process_whatsapp_message(Bot.msg_queue.pop(0), Bot)
            print("traitement")
            return jsonify({"status": "ok"}), 200
        else:
            # if the request is not a WhatsApp API event, return an error
            return (
                jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
                404,
            )
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        return jsonify({"status": "error", "message": "Invalid JSON provided"}), 400


# Required webhook verifictaion for WhatsApp
def verify():
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        print("ha",mode,token)
        if mode == "subscribe" and token == current_app.config["VERIFY_TOKEN"]:
            # Respond with 200 OK and challenge token from the request
            logging.info("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            logging.info("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        logging.info("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400


@webhook_blueprint.route("/webhook", methods=["POST", "GET"])
@signature_required
def webhook(Bots=Bot):
    if request.method == "GET":
        return verify()
    elif request.method == "POST":
        return handle_message(Bots)
