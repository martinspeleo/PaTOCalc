import datetime
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.template import RequestContext

from calc.forms import FormGenerator

@login_required
def home_page(request):
    ctx = {'user' : request.user, 'forms' : FormGenerator.objects.all() }
    return render_to_response('calc/home.html', ctx)

@login_required
def submit_new_form(request):
    ctx = {'user' : request.user, 'form' : FormGenerator }
    return render_to_response('calc/submit_form.html', ctx)
