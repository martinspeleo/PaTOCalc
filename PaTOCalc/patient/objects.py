import json


class Patient(json.JSONEncoder):
    hos_num = None

    def getId(self):
        return self.hos_num

    def setHosnum(self, hos_num):
        self.hos_num = hos_num

    def getObservation(self, name):
        if name in self.obs:
            return self.obs[name]
        try:
            method = 'get' + name
            return getattr(self, method)()
        except AttributeError:
            pass

        return None

    def __str__(self):
        return self.hos_num


class OpenEyesPatient(Patient):

    def default(self, o):
        return o.__dict__

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def setupFromDefinition(self, definition):
        hos_num = self._getIdentifierFromDefinition(definition)

        self.setHosnum(hos_num)

        self.parseDefinition(definition)

    def _getIdentifierFromDefinition(self, definition, label="Hospital Number"):
        for id in definition['identifier']:
            if (id['label'] == label):
                return id['value']
        return None

    def parseDefinition(self, definition):
        self.last_name = definition['name'][0]['family'][0]
        self.first_name = definition['name'][0]['given'][0]
        self.title = definition['name'][0]['prefix'][0]

    def __str__(self):
        return self.last_name + ',' + self.first_name + ' (' + self.title + ')'

