from datetime import datetime

import app.utils.whatsapp_utils
import perso.BotUtils as Utils
import perso.accessheet as asheet

sheet = asheet.getSheet()

class Client(object):

    def __init__(self, id, numero, prenom, chambre, adresse, creation_state = "0", actual_state = ""):
        self._prenom = prenom
        self._numero = numero
        self._chambre = chambre
        self._adresse = adresse
        self._commandes = []
        self._id = id
        self._creation_state = creation_state
        self._actual_state = actual_state
        self._last_message_bot = datetime.utcnow()

    @property
    def prenom(self):
        return self._prenom

    @property
    def last_message_bot(self):
        return self._last_message_bot

    @last_message_bot.setter
    def last_message_bot(self,time):
        self._last_message_bot = time

    @property
    def adresse(self):
        return self._adresse

    @adresse.setter
    def adresse(self, adresse):
        self._adresse = adresse

    @property
    def actual_state(self):
        return self._actual_state

    @actual_state.setter
    def actual_state(self, state):
        self._actual_state = state

    @prenom.setter
    def prenom(self,prenom):
        self._prenom = prenom

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self,nom):
        self._nom = nom

    @property
    def numero(self):
        print(self._numero)
        return self._numero
    @numero.setter
    def numero(self, numero):
        self._numero = numero
    @property
    def chambre(self):
        return self._chambre

    @chambre.setter
    def chambre(self,chambre):
        self._chambre = chambre

    @property
    def creation_state(self):
        return self._creation_state

    @creation_state.setter
    def creation_state(self, state):
        self._creation_state = state

    def creerClient(self):
        if self._id >= sheet.col_values(1):
            asheet.set_id(id, id)
            asheet.set_numero(id, self._numero)
            asheet.set_prenom(id, self._prenom)
            asheet.set_chambre(id, self._chambre)
            asheet.set_points(id, 0)

    @property
    def commandes(self):
        return self._commandes

    def addCommande(self,commande):
        self._commandes.append(commande)

    def showAllo(self, Bot):
        self.sendMessage(Utils.send_list_msg(self._numero, "Voici les Allos tu peux toujours retrouver la liste en tappant 'Allo'", "Clique ici !", Bot.allos))

    def sendMessage(self,msg):
        data = Utils.get_text_message_input(self._numero, msg)
        Utils.send_message(data)

    def isAdmin(self):
        admin = ["+33663050830", "+33782625602", "+33695601344"]
        if self._numero in admin:
            return True
        return False

    def isModo(self):
        modo = ["+33769392207", "+33663050830", "+33768358540", "+33782663583", "+33643683363", "+33768787079", "+33783859041", "+33695355751",
                "+33614511076", "+33695601344", "+33781220548", "+33767474393", "+33623989823", "+33783337740", "+33776698726", "+33698354063",
                "+33620910825", "+33667485143", "+33782625602", "+33766016783", "+33768208857"]
        if self.numero in modo:
            return True
        return False
