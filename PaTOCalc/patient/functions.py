from django.conf import settings

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
        print("here")
        # do OE search and return patient results
        return {'id': 'OE - ' + str(search_term)}
    else:
        raise Exception('unregonised patient search configuration')