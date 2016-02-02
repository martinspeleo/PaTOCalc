from datetime import date, datetime


class Patient(object):
    """
    Base Patient object to encapsulate data retrieved from external source
    """
    hos_num = None

    def __init__(self):
        self.obs = {
            'height': 170,
            'age': 56,
            'sex': 'm',
            'weight': 70
        }

    def getId(self):
        return self.hos_num

    def getHosnum(self):
        return self.hos_num

    def setHosnum(self, hos_num):
        self.hos_num = hos_num

    def getObservation(self, name, **kwargs):
        """
        Potentially unneccessary wrapper function for retrieving patient observations

        :param name:
        :param kwargs:
        :return:
        """
        try:
            method = 'get' + name
            return getattr(self, method)(**kwargs)
        except AttributeError:
            pass

        if name.lower() in self.obs:
            return self.obs[name]

        return None

    def getHeight(self, units='m'):
        if (units == 'm'):
            return self.getObservation('height')
        elif (units == 'cm'):
            return self.getObservation('height') * 100
        elif (units == 'inches'):
            return (self.getObservation('height') * 100) / 2.54
        raise Exception('invalid units: ' + units)

    def __str__(self):
        return self.hos_num


class OpenEyesPatient(Patient):
    """
    Patient object instantiated from OpenEyes JSON API response
    """
    def __init__(self):
        super(OpenEyesPatient, self).__init__()
        self.obs = {}

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def setupFromDefinition(self, definition):
        hos_num = self._getIdentifierFromDefinition(definition)

        self.setHosnum(hos_num)

        self.parseDefinition(definition)

    def _getIdentifierFromDefinition(self, definition, label="Hospital Number"):
        """
        Convenience wrapper for retrieving ids from the OpenEyes JSON definition of a patient
        :param definition: OpenEyes JSON API patient definition
        :param label: ID to be retrieved
        :return: string the id value or None
        """
        for id in definition['identifier']:
            if (id['label'] == label):
                return id['value']
        return None

    def parseDefinition(self, definition):
        """
        Set Patient attributes from the given OE JSON API patient definition

        :param definition:
        :return:
        """

        self.last_name = definition['name'][0]['family'][0]
        self.first_name = definition['name'][0]['given'][0]
        self.title = definition['name'][0]['prefix'][0]

        self.dob = datetime.strptime(definition['birthDate'], '%Y-%m-%d')
        self.obs['sex'] = definition['gender']['coding'][0]['code'].lower()

    def __str__(self):
        """
        HSCIC standard for displaying patient name
        :return:
        """
        return self.last_name + ', ' + self.first_name + ' (' + self.title + ')'

    def getage(self):
        """
        Obs method for calculating patient age
        :return:
        """
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))


