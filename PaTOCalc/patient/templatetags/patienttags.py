from django import template
from django.conf import settings
from ..functions import get_openeyes_patient

register = template.Library()

@register.simple_tag(takes_context=True)
def current_patient(context):
    request = context['request']
    print("here")
    if not hasattr(settings, 'PATIENT_SOURCE'):
        return request.session.get('current_patient', None)
    elif settings.PATIENT_SOURCE == 'openeyes':
        return get_openeyes_patient(request)
    else:
        raise Exception('unregonised patient source configuration')