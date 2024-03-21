import perso.accessheet as asheet
import perso.Client as Client
import perso.accessheet_allo as asheet_allo
from datetime import datetime
import time
import mysql.connector

class Bot(object):

    def __init__(self):
        self._isOn = True
        self._sheet = asheet.getSheet()
        #self._clients = []
        self._clients = self.chargerClient()
        self._clientsInitial = self.clients.copy()
        self._allos = self.chargerAllo()
        self._menu = self.chargerMenu()
        self._time_on = datetime.now()
        self._waiting = []
        self._msg_queue = []

    def addMsg(self, msg):
        self._msg_queue.append(msg)

    @property
    def msg_queue(self):
        return self._msg_queue

    @property
    def connexion(self):
        return self._connexion

    @property
    def waiting(self):
        return self._waiting

    def addWaiting(self, commande):
        self._waiting.append(commande)

    @property
    def isOn(self):
        return self._isOn

    @isOn.setter
    def isOn(self, value):
        self._isOn = value

    @property
    def datetime(self):
        return self._time_on

    @property
    def clients(self):
        print(self._clients)
        return self._clients

    @property
    def allos(self):
        print(self._allos)
        return self._allos

    def chargerClient(self):
        print("Chargement des clients")
        clients = []
        n = self._sheet.col_values(1)
        print("Nombre de colonne"  + str(n))
        for i in range(2,len(n)+1):
            row = self._sheet.row_values(i)
            print(row)
            client = Client.Client(row[0], str(row[1]), row[2], row[3], row[4], str(row[5]))
            time.sleep(0.8)
            clients.append(client)
            del client
        return clients

    def saveClient(self):
        print(self._clientsInitial, self.clients)
        for i in self._clients:
            if i not in self._clientsInitial and i.creation_state == 4:
                try:
                    asheet_allo.ecrire("PERSONNE", ["None", str(i.numero), i.prenom, i.chambre, i.adresse, str(i.creation_state), i.actual_state])
                    self._clientsInitial.append(i)
                except Exception as e:
                    print(e)
                    pass

    def create_personne(self, id, numero, prenom, nom, chambre, annee):
        self._sheet.set_id(id, id)
        self._sheet.set_numero(id, numero)
        self._sheet.set_prenom(id, prenom)
        self._sheet.set_chambre(id, chambre)

    def addClient(self, client):
        self._clients.append(client)

    def removeClient(self, client):
        self._clients.remove(client)

    def getClientByNumero(self, numero):
        for i in self._clients:
            if i.numero == numero:
                return i
        print("Client not found")
        return False

    def getAlloByName(self, name):
        for i in self._allos:
            if i.name == name:
                return i
        return None

    def chargerAllo(self):
        return []

    def addAllo(self,allo):
        for i in allo:
            self._allos.append(i)

    def isAlloActif(self):
        for i in self._allos:
            if i.isOn:
                return True
        return False

    def chargerMenu(self):
        return  []

