class Allo(object):

    def __init__(self, id, name, etat, quantite,description = ""):
        self._clients = []
        self._id = id
        self._description = description
        self._name = name
        self._isOn = etat
        self._quantite = quantite

    @property
    def quantite(self):
        return self._quantite

    @quantite.setter
    def quantite(self, quantite):
        self._quantite = quantite

    @property
    def isOn(self):
        return self._isOn

    @isOn.setter
    def isOn(self, value):
        self._isOn = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def clients(self):
        return self._clients