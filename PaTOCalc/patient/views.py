from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import PatientSearchForm
from .functions import set_current_patient, clear_current_patient

# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"

class PatientSearchView(FormView):
    template_name = "search.html"
    form_class = PatientSearchForm

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        # this should not work like this, because we should actually search first
        set_current_patient(self.request, {'id': form.cleaned_data['search_term']})

        return super(PatientSearchView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PatientSearchView, self).get_context_data(**kwargs)
        clear_current_patient(self.request)
        return context
