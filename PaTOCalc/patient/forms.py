from django import forms

class PatientSearchForm(forms.Form):
    search_term = forms.CharField(max_length=40)


