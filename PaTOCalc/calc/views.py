import datetime
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from calc.forms import AddFormGenerator
from calc.models import FormGenerator, FormInstance

@login_required
def admin_home_page(request):
    ctx = {'user' : request.user, 'forms' : FormGenerator.objects.all() }
    return render_to_response('calc/home.html', ctx)

@login_required
def submit_new_form(request):
    ctx = {'user' : request.user, 'form' : AddFormGenerator }
    return render_to_response('calc/submit_form.html', ctx)

@login_required
def new_form_instance(request, fi_pk, mrn):
    fi = get_object_or_404(FormInstance, pk = fi_pk)
    #patient = get_patient ...
    ctx = {'user' : request.user, 'form': fi}
    return render_to_response('calc/form_instance.html', ctx)
