from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import base64


def get_current_patient(request):
    return request.session.get('current_patient', None)

def set_current_patient(request, patient):
    request.session['current_patient'] = patient

def clear_current_patient(request):
    request.session['current_patient'] = None

def search_for_patient(search_term):
    if not hasattr(settings, 'PATIENT_SOURCE'):
        return {'id': search_term}
    elif settings.PATIENT_SOURCE == 'openeyes':
        url = settings.OPENEYES_URL + '/api/Patient?identifier=' + str(search_term)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.get(url,
                                auth=HTTPBasicAuth(settings.OPENEYES_USER, settings.OPENEYES_PASSWORD),
                                headers=headers).json()

        if (response['entry']):
            entries = response['entry']
            if (len(entries) > 1):
                return {'id': 'OE - Multiple results not implemented yet for search ' + str(search_term)}
            elif (len(entries) == 1):
                patient = entries[0]['content']
                return {
                    'id': patient['name'][0]['given'][0] + ' ' + patient['name'][0]['family'][0]
                }
            else:
                return None
        else:
            raise Exception('search not available')
    else:
        raise Exception('unregonised patient search configuration')