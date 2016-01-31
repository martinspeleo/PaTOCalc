from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PatientSearchForm
from .functions import set_current_patient, clear_current_patient, search_for_patient

# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"

@method_decorator(login_required, name='dispatch')
class PatientSearchView(FormView):
    template_name = "search.html"
    form_class = PatientSearchForm

    def get_success_url(self):
        return reverse('calc:choose-generator')

    def form_valid(self, form):
        # this should not work like this, because we should actually search first
        patient = search_for_patient(form.cleaned_data['search_term'])
        set_current_patient(self.request, patient)

        return super(PatientSearchView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PatientSearchView, self).get_context_data(**kwargs)
        clear_current_patient(self.request)
        return context
