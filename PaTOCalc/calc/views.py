import datetime
import json

from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from calc.forms import AddFormGenerator
from calc.models import FormGenerator, FormInstance

@staff_member_required
def admin_home_page(request):
    ctx = {'user' : request.user, 'forms' : FormGenerator.objects.all() }
    return render_to_response('calc/home.html', ctx)

@staff_member_required
def submit_new_form(request):
    form = AddFormGenerator(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        newForm = form.save(commit=False)
        newForm.requester = request.user
        newForm.status = '0'
        newForm.save()
        return HttpResponseRedirect(reverse('home')) 

    ctx = {'user' : request.user, 'form' : form }
    return render_to_response('calc/submit_form.html', ctx, context_instance=RequestContext(request))


@login_required
def new_form_instance(request, fg_pk, mrn):
    fg = get_object_or_404(FormGenerator, pk = fg_pk)
    #patient = get_patient ...

    form = fg.get_form()(request.POST)
    if request.method == 'POST' and form.is_valid():
        fi = FormInstance(author = request.user,
                          content = json.dumps(form.cleaned_data),
                          created_date = datetime.datetime.now(),
                          form_generator = fg)
        fi.save()
        return redirect('pdf_viewer', fi.pk)
    ctx = {'user' : request.user, 'form': form}
    return render(request,'calc/form_instance.html', ctx)

@method_decorator(login_required, name='dispatch')
class CalculatorListView(ListView):
    model = FormGenerator
