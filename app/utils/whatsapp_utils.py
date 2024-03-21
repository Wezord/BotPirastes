import logging
import time
import cProfile
from datetime import datetime

from flask import current_app, jsonify
import json
import requests
from perso import accessheet as asheet
from perso import accessheet_allo as asheet_allo
# from app.services.openai_service import generate_response
import re

#Moi
import perso.BotUtils as Utils
import perso.Client as Client
import perso.Allo as Allo
import perso.Commande as Commande

def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def generate_response(response):
    # Return text in uppercase
    return response.upper()

def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body, Bot):

    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    print(message)

    num = "+" + message["from"]
    id = asheet.is_numero(num)
    print("L'id est : " + str(id))

    if datetime.now() < Bot.datetime:
        return

    if message["timestamp"] != None and abs(datetime.utcnow() - datetime.utcfromtimestamp(int(message["timestamp"]))).total_seconds() > 180:
        return

    admin = ["+33663050830", "+33782625602", "+33695601344"]

    if not Bot.isOn and num not in admin:
        data = Utils.get_text_message_input(num, "Désolé, les Allos ne sont pas ouvert !")
        Utils.send_message(data)
        return

    print("Le numéro est : " + num)

    if not Bot.getClientByNumero(num):

        print("Création client")
        client = Client.Client(None, num,None,None, None)
        Bot.addClient(client)

    else :
        client = Bot.getClientByNumero(num)
        print("Le client est : " , client)

    print("State ", client.creation_state, client.creation_state == "4")

    try :
        Utils.createClient(client, message['text']['body'], Bot)
    except Exception as e:
        print(e)

    print("Caca")
    print("le temps est : ", abs(datetime.utcnow() - client.last_message_bot).total_seconds())

    '''
    if abs(datetime.utcnow() - client.last_message_bot).total_seconds() > 180:
        print("Message envoyé trop tard")
        client.showAllo(Bot)
        client.last_message_bot = datetime.utcnow()
        return
    '''

    print("Ca passe")
    client.last_message_bot = datetime.utcnow()

    if 'text' in message and 'body' in message['text']:

        message_body = message['text']['body'].upper()
        print(f"Message Body: {message_body}")
        if(client._actual_state == "changement adresse"):
            Utils.changerAdresse(client, message_body, Bot)

        elif(client._actual_state == "PETIT DEJ"):
            print("Commande")
            client.actual_state = ""
            commande = Commande.Commande(client, Bot.getAlloByName("PETIT DEJ"), message_body)
            client.addCommande(commande)
            Utils.confAllo(client, Bot.getAlloByName("PETIT DEJ"), Bot.getAlloByName("PETIT DEJ").quantite)

        elif(len(client._actual_state.split()) > 1 and client._actual_state.split()[0] == "QUANTITE"):
            print("Quantite")
            client.actual_state = ""
            client.commandes[-1].quantite = message_body
            Utils.confAllo(client, Bot.getAlloByName(client.commandes[-1].name), Bot.getAlloByName(client.commandes[-1].name))

        elif message_body == "ALLO" and client._creation_state == "4":
            if Bot.isAlloActif():
                try:
                    client.showAllo(Bot)
                except Exception as e:
                    print("Erreur", e)
                print("On montre les allos")
            else:
                client.sendMessage("Il n'y a pas d'allo actif")
                print("pas d'allo")


        elif message_body.split()[0] == "TERMINER":
            if message_body == "TERMINER BOT" and client.isAdmin():
                Bot.saveClient()
                print("Saving client")
            elif len(message_body.split()) > 1 and message_body.split()[1] == "ALLO" and client.isModo():
                if len(message_body.split()) < 3:
                    client.sendMessage("Format incorrect ! Il doit être de la forme : Terminer Allo 'Nom de l'Allo'")
                    return
                name = ""
                for i in range(len(message_body.split()[2:]) - 1):
                    name += message_body.split()[2:][i] + " "
                name += message_body.split()[-1]
                print("Allo termine")
                Bot.getAlloByName(name).isOn = False

        elif message_body.split()[0] == "OPEN":
            if message_body.split()[1] == "ALLO" and client.isModo():
                if len(message_body.split()) < 3:
                    client.sendMessage("Format incorrect ! Il doit être de la forme : Open Allo 'Nom de l'Allo'")
                    return
                print("ALLO OUVERT")
                client.sendMessage("ALLO OUVERT")
                name = ""
                for i in range(len(message_body.split()[2:])-1):
                    name += message_body.split()[2:][i] + " "
                name += message_body.split()[-1]
                if name in [i.name for i in Bot.allos]:
                    
                print(name, name == "WRAP JAMBON")
                if Bot.getAlloByName(name) == None:
                    client.sendMessage("Tromper de nom d'Allo")
                    return
                Bot.getAlloByName(name).isOn = True

        elif message_body.split()[0] == "LIVRER" and client.isModo():
            #Ecrire un allo comme terminer
            if len(message_body.split()) < 3:
                client.sendMessage("Format incorrect ! Il doit être de la forme : Livrer 'Numero du client' 'Nom de l'allo'")
                return
            name = ""
            for i in range(len(message_body.split()[2:]) - 1):
                name += message_body.split()[2:][i] + " "
            name += message_body.split()[-1]
            client2 = Bot.getClientByNumero(message_body.split()[1])
            if not client2:
                client.sendMessage("Tromper de numéro")
                return

            for i in client2.commandes:
                print(i.allo.name)
                if i.allo.name == name:
                    print("Oui")
                    client2.commandes.remove(i)
                    client2.sendMessage("Prépare toi on arrive !")

            print("Allo livrer !")
            return

        elif message_body.split()[0] == "QUANTITE" and client.isModo():
            # Modifier la quantite d'un Allo
            if len(message_body.split()) < 3:
                client.sendMessage("Format incorrect ! Il doit être de la forme : Quantite 'Quantite' 'Nom de l'Allo'")
                return
            name = ""
            for i in range(len(message_body.split()[2:]) - 1):
                name += message_body.split()[2:][i] + " "
            name += message_body.split()[-1]
            print("Quantite modifie !")
            client.sendMessage("Quantite modifie !")
            try:
                Bot.getAlloByName(name).quantite = int(message_body.split()[1])
            except Exception as e:
                print(e)
            return

        elif message_body == "BOT OFF" and client.isAdmin():
            # Eteindre le bot
            Bot.isOn = False
            Bot.saveClient()
            print("Bot éteint")
            return

        elif message_body == "BOT ON" and client.isAdmin():
            Bot.isOn = True
            print("Bot allumé")
            return

        elif message_body == "BOT ON BROADCAST" and client.isAdmin():
            #Allumer le bot en envoyant un message à tout le monde
            Bot.isOn = True
            for i in Bot.clients:
                i.sendMessage("Les Allos des Pir'As'tes sont ouvert ! Viens voir ce que l'on propose en écrivant Allo !")
            print("Bot allumé")
            return

        elif message_body.split()[0] == "BROADCAST" and client.isModo():
            # Envoyer un message à tout le monde
            for i in Bot.clients:
                i.sendMessage(message_body)
            return

        elif message_body.split()[0] == "ADDALLO" and client.isModo():
            #Créer un Allo
            if len(message_body.split()) < 3:
                client.sendMessage("Format incorrect ! Il doit être de la forme : ADDALLO 'Nom de l'Allo' 'Quantite'")
                return
            name = ""
            for i in range(len(message_body.split()[2:]) - 1):
                name += message_body.split()[2:][i] + " "
            name += message_body.split()[-1]
            new_allo = Allo.Allo(5, name, True, message_body.split()[2])
            Bot.addAllo([new_allo])
            return

        else:
            Utils.sendFailedMessage(client)

    elif message["interactive"]["type"] == "button_reply":

        message_body = message["interactive"]["button_reply"]["title"].upper()

        if message_body == "ALLO":
            client.showAllo(Bot)
        elif message_body == "CONFIRMER":

            if client.commandes != [] and client.commandes[-1].allo.isOn:
                try:
                    #client.commandes[-1].ligne = Utils.creerAllo(client, client.commandes[-1], Bot)
                    Utils.creerAllo(client, client.commandes[-1], Bot)
                except Exception as e:
                    print("Surcharge des services")
            elif client.commandes != [] and not client.commandes[-1].allo.isOn:
                client.sendMessage("Cette allo n'est pas disponible petit malin")
            else:
                client.sendMessage("Vous n'avez pas de commandes")

        elif message_body == "CHANGER D'ADRESSE":
            Utils.changerAdresse(client, message_body, Bot)

            client.commandes.pop()

        elif message_body == "ANNULER":
            client.commandes.pop()

    elif message["interactive"]["type"] == "list_reply":

        message_body = message["interactive"]["list_reply"]["title"].upper()
        bool = True
        for i in Bot.allos:
            if i.name == message_body:
                for i in client.commandes:
                    if i.allo.name == message_body:
                        bool = False
                if bool:

                    client.actual_state = "QUANTITE " + message_body

                    if message_body == "PETIT DEJ":
                        client.sendMessage("A quelle heure veux tu recevoir ton petit dej ?")
                        client.actual_state = "PETIT DEJ"
                        return
                    print("Commande")
                    commande = Commande.Commande(client, Bot.getAlloByName(message_body))
                    client.addCommande(commande)
                    client.sendMessage("Combien en veux-tu ?")
                else:
                    client.sendMessage("Vous avez déjà une commande de ce type en cours !")

    #response = generate_message_custom(message_body, id, num)
    #data = get_text_message_input(num, response)
    #send_message(data)
    commande = ""
    del client
    del commande
    del message_body

def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
