from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import json
from .objects import Patient, OpenEyesPatient


def get_openeyes_patient(request):
    id = request.session.get('current_patient', None)
    if id is not None:
        url = id
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.get(url,
                                auth=HTTPBasicAuth(settings.OPENEYES_USER, settings.OPENEYES_PASSWORD),
                                headers=headers)

        if response.status_code != requests.codes.ok:
           response.raise_for_status()

        result = response.json()
        patient = OpenEyesPatient()
        patient.setId(id)
        patient.setupFromDefinition(result)
        return patient
    return None

def get_current_patient(request):
    if not hasattr(settings, 'PATIENT_SOURCE'):
        return request.session.get('current_patient', None)
    elif settings.PATIENT_SOURCE == 'openeyes':
        return get_openeyes_patient()
    else:
        raise Exception('unregonised patient source configuration')


def set_current_patient(request, patient):
    request.session['current_patient'] = patient.getId()

def clear_current_patient(request):
    request.session['current_patient'] = None

def search_for_patient(search_term):
    if not hasattr(settings, 'PATIENT_SOURCE'):
        patient = Patient()
        patient.setHosnum(search_term)
        return patient
    elif settings.PATIENT_SOURCE == 'openeyes':
        return openeyes_search(search_term)
    else:
        raise Exception('unregonised patient search configuration')

def openeyes_search(search_term):
    url = settings.OPENEYES_URL + '/api/Patient?identifier=' + str(search_term)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.get(url,
                            auth=HTTPBasicAuth(settings.OPENEYES_USER, settings.OPENEYES_PASSWORD),
                            headers=headers)

    if response.status_code != requests.codes.ok:
       response.raise_for_status()

    result = response.json()

    if 'entry' in result:
        entries = result['entry']
        if (len(entries) > 1):
            return {'id': 'OE - Multiple results not implemented yet for search ' + str(search_term)}
        elif (len(entries) == 1):
            patient = OpenEyesPatient(entries[0]['content'])
            patient.setId(entries[0]['id'])
            return patient
        else:
            return None
    else:
        raise Exception('Unexpected search response' + response.text)