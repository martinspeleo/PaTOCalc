import datetime
import json
import sys
from django.views.decorators.csrf import csrf_exempt
from random import randint
from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from calc.forms import AddFormGenerator
from calc.models import FormGenerator, FormInstance

from patient.functions import get_current_patient


@staff_member_required
def admin_home_page(request):
    ctx = {'user': request.user, 'forms': FormGenerator.objects.all()}
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

    ctx = {'user': request.user, 'form': form}
    return render_to_response('calc/submit_form.html', ctx, context_instance=RequestContext(request))


@login_required
def new_form_instance(request, fg_pk, mrn):
    fg = get_object_or_404(FormGenerator, pk=fg_pk)

    cp = get_current_patient(request)
    # TODO: Would be better to pickle the patient
    patient = {
        'hos_num': cp.getHosnum(),
        'name': str(cp),
        'age': cp.getObservation('age'),
        'sex': cp.getObservation('sex')
    }

    form = fg.get_form()(patient)
    if request.method == 'POST':
        form = fg.get_form()(request.POST)
        if form.is_valid():
            fi = FormInstance(author=request.user,
                              content=json.dumps(form.cleaned_data),
                              created_date=datetime.datetime.now(),
                              form_generator=fg,
                              patient_data=json.dumps(patient))

            fi.save()
            return redirect('pdf_viewer', fi.pk)

    ctx = {'user': request.user, 'form': form, 'fg_pk': fg_pk, 'mrn': mrn,
           'patient': patient, 'fg': fg}
    return render(request, 'calc/form_instance.html', ctx)


@login_required
def evaluate(request, fg_pk, mrn):
    fg = get_object_or_404(FormGenerator, pk=fg_pk)
    inputs = {}
    for key in [x['name'] for x in fg.get_data() if x['type'] == 'num']:
        try:
            inputs[key] = float(request.GET[key][0])
        except:
            pass
    for key in [x['name'] for x in fg.get_data() if x['type'] == 'select']:
        try:
            inputs[key] = request.GET[key][0]
        except:
            pass
    result = fg.evaluate(inputs)
    return JsonResponse(result)


@login_required
@csrf_exempt
def check_my_code(request):
    # if request.method != 'POST':
    #    return HttpResponse('<h1>Page was found</h1>')

    fields = json.loads(request.POST['fields'])
    mycode = '# This is a code checking example \n'
    mycode += '# Random numbers were used to run the code. \n \n'
    mycode += '# Input fields with random numbers \n'

    for field in fields:
        if field['type'] == 'num':
            mycode += '{0} = {1} \n'.format(field['label'], randint(0, 9))

    mycode += '\n\n# Output fields  \n'
    for field in fields:
        if field['type'] == 'output':
            mycode += '{0} = "" \n'.format(field['label'])

    mycode += '\n\n# Your code \n'
    mycode += request.POST['mycode']

    mycode += '\n\n# Output fields results  \n'
    for field in fields:
        if field['type'] == 'output':
            mycode += 'print({0}) \n'.format(field['label'], '')

    output = 'That was the executed code : \n{0}'.format(mycode)
    try:
        from cStringIO import StringIO
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec (mycode)
        sys.stdout = old_stdout
        output += 'That was the results of your code : \n{0}'.format(redirected_output.getvalue())
    except Exception as e:
        output += 'An error was found: {0}'.format(e)

    return HttpResponse(output)


@method_decorator(login_required, name='dispatch')
class CalculatorListView(ListView):
    model = FormGenerator
