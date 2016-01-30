from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import PatientSearchForm

# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"

class PatientSearchView(FormView):
    template_name = "search.html"
    form_class = PatientSearchForm

