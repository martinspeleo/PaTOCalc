from django.forms import ModelForm
from calc.models import FormGenerator

# Create the form class.
class AddFormGenerator(ModelForm):
    
	class Meta:
		model = FormGenerator
		fields = ['title', 'requirements', 'risks']
