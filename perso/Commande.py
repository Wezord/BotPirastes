import datetime
import app.utils.whatsapp_utils
import perso.BotUtils as Utils
import perso.accessheet_allo as asheet_allo

class Commande(object):

    def __init__(self, client, allo, quantite = 1, heure = None, ligne = None):
        self._date = datetime.date.today()
        self._debut_time = datetime.time
        self._fin_time = 0
        self._client = client
        self._allo = allo
        self._etat = "en cours"
        self._ligne = ligne
        self._heure = heure
        self._quantite = quantite

    @property
    def allo(self):
        return self._allo

    @property
    def heure(self):
        return self._heure

    @heure.setter
    def heure(self, heure):
        self._heure = heure

    @property
    def quantite(self):
        return self._quantite

    @quantite.setter
    def quantite(self, quantite):
        self._quantite = quantite

    @property
    def ligne(self):
        return self._ligne

    @ligne.setter
    def ligne(self,ligne):
        self._ligne = ligne

    @property
    def client(self):
        return self._client

    def finish(self,ligne):
        self._fin_time = datetime.time
        self._debut_time = "fini"
        asheet_allo.endAllo(self.allo.name.split()[0],str(ligne))

    def notifier(self):
        data = Utils.get_text_message_input(self._client.numero, "Votre commande est prête pour l'allo : " + self.allo.name + " ! Préparez vous !")
        Utils.send_message(data)