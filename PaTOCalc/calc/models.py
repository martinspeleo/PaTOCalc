from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.forms.forms import Form
from django.forms.fields import CharField, FloatField, ChoiceField, MultipleChoiceField

import json


class FormGenerator(models.Model):
    FORM_STATUS = (
	('0' , 'In progress'),
	('1' , 'Submitted'),
	('2' , 'Under development'),
	('3' , 'Under testing'),
	('4' , 'Authorized'),
    )
    
    # Submission
    title = models.CharField(max_length=30)
    status = models.CharField(max_length=1, choices=FORM_STATUS)
    requester = models.ForeignKey(User, blank=True, related_name='requested_forms')
    requirements = models.TextField(blank=True, null=True)
    risks = models.TextField(blank=True, null=True)
    
    # Dates
    submited_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    under_dev_date = models.DateTimeField(blank=True, null=True)
    under_testing_date = models.DateTimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)

    # Implementation
    html = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    tesing_report = models.TextField(blank=True, null=True)
    developer = models.ForeignKey(User, blank=True, null=True, related_name='forms_for_dev')
    tester = models.ForeignKey(User, blank=True, null=True, related_name='forms_for_testing')

    
    def get_data(self):
        if self.html:
            return json.loads(self.html)
        return []
    
    def get_form(self):    
        class DynamicForm(Form):
            def __init__(s, *args, **kwargs):
                super(DynamicForm, s).__init__(*args, **kwargs)
                for item in self.get_data():
                    if item["type"] == "num":
                        s.fields[item["name"]] = FloatField(label=item["label"])
                    elif item["type"] == "text":
                        s.fields[item["name"]] = CharField(label=item["label"], max_length=255)
                    elif item["type"] == "dsc":
                        s.fields[item["name"]] = CharField(label=item["label"], max_length=255)
                    elif item["type"] == "select":
                        options = [(element['value'], element['label']) for element in item['values']]
                        s.fields[item["name"]] = ChoiceField(label=item["label"], choices=options)
                    elif item["type"] == "multiselect":
                        options = [(element['value'], element['label']) for element in item['values']]
                        s.fields[item["name"]] = MultipleChoiceField(label=item["label"], choices=options)
        return DynamicForm

class FormInstance(models.Model):
    author = models.ForeignKey(User)
    content = models.TextField()
    created_date = models.DateTimeField()
    form_generator = models.ForeignKey('FormGenerator', blank=True, null=True)
    
    def get_data(self):
        return json.loads(self.content)

