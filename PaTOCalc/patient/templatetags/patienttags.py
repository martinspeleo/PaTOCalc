from django import template
from django.conf import settings
from ..functions import get_current_patient, get_openeyes_patient

register = template.Library()

@register.simple_tag(takes_context=True)
def current_patient(context):
    request = context['request']
    return get_current_patient(request)
