
def get_current_patient(request):
    return request.session.get('current_patient', None)

def set_current_patient(request, patient):
    request.session['current_patient'] = patient

def clear_current_patient(request):
    request.session['current_patient'] = None