import logging
import mysql.connector
from flask import current_app, jsonify
import json
import requests
from datetime import datetime
# from app.services.openai_service import generate_response
import re
import perso.accessheet as asheet
import perso.accessheet_allo as asheet_allo
import perso.Client as Client

def creerAllo(client, commande, Bot):


    asheet_allo.openAllo(commande.allo.name.split()[0], str(asheet_allo.getLen(commande.allo.name.split()[0]) + 1))
    if commande.allo.name == "Taxi":
        data = get_text_message_input(client._numero,
                                      "Votre place est reservé  ! On vous attends à la fin de la soirée mde côté gymnase vous avez 5 mins max !")
    else:
        data = get_text_message_input(client._numero,"Votre " + commande.allo.name + " arrive ! Un message sera envoyé quand elle sera prête ! ")
    send_message(data)


    print("2")

    if commande.heure == None:
        commande.heure = ""

    host = '193.203.168.6'
    user = 'u760277800_ladminpirates'
    password = 'Fuckmaloleroidespirates44$'
    database = 'u760277800_allo_pirastes'
    raise_on_warnings = True

    connexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        raise_on_warnings=raise_on_warnings
    )
    if connexion.is_connected():
        requete_select = "INSERT INTO allo (Prenom, Chambre, Adresse, Nom_Allo, Heure_validation, Quantite, Heure, Numero) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        valeurs = (client.prenom, client.chambre, client.adresse, commande.allo.name, str(datetime.now()), commande.quantite, commande.heure, client.numero)

        print("2")
        curseur = connexion.cursor()
        curseur.execute(requete_select, valeurs)

        print("3")
        connexion.commit()
        curseur.close()
        connexion.close()
    else:
        print("Probleme")

    '''
    try:
        ligne = asheet_allo.ecrire(commande.allo.name.split()[0], [client.prenom, client.chambre, client.adresse, commande.allo.name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), client.numero, commande.heure])
        asheet_allo.openAllo(commande.allo.name.split()[0], str(ligne))
    except Exception as e:
        print(e)
        Bot.waiting.append([client,commande])
        raise Exception
    return ligne
    '''
    return
def reqTemplate(response_data):
    url = 'https://graph.facebook.com/v18.0/181790545019298/messages'
    access_token = current_app.config['ACCESS_TOKEN']  # Remplacez par votre jeton d'accès

    # Ajouter l'en-tête Authorization avec le jeton d'accès
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Effectuer la requête POST
    response = requests.post(url, headers=headers, json=response_data)

    # Afficher le statut de la requête et la réponse JSON
    print(f"Status Code: {response.status_code}")
    print(response.json())

def confAllo(client, allo):

    host = '193.203.168.6'
    user = 'u760277800_ladminpirates'
    password = 'Fuckmaloleroidespirates44$'
    database = 'u760277800_allo_pirastes'
    raise_on_warnings = True

    connexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        raise_on_warnings=raise_on_warnings
    )
    if connexion.is_connected():
        curseur = connexion.cursor()
        selection_query = "SELECT qte FROM dispo WHERE id = %s"

        try :
            # Exécuter la requête SELECT
            curseur.execute(selection_query, allo.name)

        # Récupérer la première ligne du résultat
            resultat = curseur.fetchone()

            if resultat:
                # La valeur de la colonne 'qte' se trouve dans la première position du tuple
                valeur_qte = resultat[0]

                print("La valeur de qte pour le nom 'pancake' est :", valeur_qte)
            else:
                print("Aucun résultat trouvé pour le nom 'pancake'.")


            print("3")
            curseur.close()
            connexion.close()
        except Exception as e:
            print(e)
            valeur_qte = 1
    else:
        print("Probleme")
        return


    if valeur_qte == 0:
        data = get_text_message_input(client.numero,
                                      "Désolé les réservations ne sont plus possibles ! Allo dépassé par son succès...")
        send_message(data)
        return

    # Remplacer "unique-postback-id" et les titres des boutons selon vos besoins
    response_data = {
        "recipient_type": "individual",
        "to": client.numero,
        "type": "interactive",
        "messaging_product": "whatsapp",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Es-tu sûr de vouloir te faire livrer l'allo : " + allo.name + " " + client.commandes[-1].quantite + " fois à l'adresse : " + client.chambre + " " + client.adresse + " ?"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "unique-postback-id-1",
                            "title": "Confirmer"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "unique-postback-id-2",
                            "title": "Changer d'adresse"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "unique-postback-id-3",
                            "title": "Annuler"
                        }
                    }
                ]
            }
        }
    }

    return reqTemplate(response_data)

def send_button_msg(num, texte, options):
    # Structure buttons à remplir
    buttons = []

    # Utilisation d'une boucle for pour remplir buttons
    for i, option in enumerate(options, start=1):
        bouton = {
            "type": "reply",
            "reply": {
                "id": f"unique-postback-id-{i}",
                "title": option.name
            }
        }
        buttons.append(bouton)

    response_data = {
        "recipient_type": "individual",
        "to": num,
        "type": "interactive",
        "messaging_product": "whatsapp",
        "interactive": {
            "type": "button",
            "body": {
                "text": texte
            },
            "action": {
                "buttons": [
                    buttons
                ]
            }
        }
    }

    return reqTemplate(response_data)

def send_list_msg(num ,texte,  titre, options ):
    # Structure buttons à remplir
    buttons = []

    # Utilisation d'une boucle for pour remplir buttons
    for i, option in enumerate(options, start=1):
        if option.isOn:
            bouton = {
                    "id": "SECTION_1_ROW_"+ str(i) + "_ID",
                    "title": option.name,
                    }
            buttons.append(bouton)

    response_data = {
        "recipient_type": "individual",
        "to": num,
        "type": "interactive",
        "messaging_product": "whatsapp",
        "interactive": {
            "type": "list",
            "body": {
                "text": texte
            },
            "action": {
              "button": "Clique-ici !",
              "sections": [
                {
                  "title": titre,
                  "rows": buttons
                }
              ]
            }
        }
    }
    return reqTemplate(response_data)

def createClient(client, message, Bot):
    print("L'état de creation est :" + str(client.creation_state))
    if client.creation_state == "0":
        print("Etape 1")
        rep = "Pour commander c'est très simple, mais pour cela tu dois bien respecter les instructions sinon rien ne sera livré ! Attends bien que le bot te réponde avant d'écrire un message et n'écrit pas des messages inutiles sinon ca ne marchera pas. Pour commander tu pourras écrire ' Allo ' mais avant il va falloir t'inscrire !"
        data = get_text_message_input(client._numero, rep)
        send_message(data)
        rep = "Quel est ton prénom ?"
        client.creation_state = "1"
    elif client.creation_state == "1":
        print("Etape 2")
        client.prenom = message
        rep = "Quel est ton numéro de chambre ?"
        client.creation_state = "2"
    elif client.creation_state == "2":
        print("Etape 3")
        client.chambre = message
        rep = "Quel est ton adresse ?"
        client.creation_state = "3"
    elif client.creation_state == "3":
        print('Etape 4')
        client.adresse = message
        data = get_text_message_input(client.numero, send_list_msg(client.numero, "Voici les Allos tu peux toujours retrouver la liste en tappant 'Allo'", "Clique ici !", Bot.allos))
        send_message(data)
        client.creation_state = "4"
        return
    else:
        return

    data = get_text_message_input(client._numero, rep)
    send_message(data)
    raise Exception

def changerAdresse(client, message, Bot):
    if(client.actual_state == "changement adresse"):
        client._adresse = message
        client.sendMessage("Votre adresse a bien été changé pour :" + message)
        client.actual_state = "4"
        client.showAllo(Bot)
    else:
        client._actual_state = "changement adresse"
        client.sendMessage("Entrer l'adresse où vous souhaitez être livré !")

def sendFailedMessage(client):
    return

def broadcast(message, Bot):
    for i in Bot.clients:
        i.sendMessage(message)
























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


def process_whatsapp_message(body,rep):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    print(message_body)

    return message_body

    # TODO: implement custom function here
    #response = rep

    #data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    #send_message(data)


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