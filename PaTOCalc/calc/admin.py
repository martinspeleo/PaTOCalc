from django.contrib import admin

from calc.models import FormGenerator

class ReneratedForms(admin.ModelAdmin):
    pass

admin.site.register(FormGenerator, ReneratedForms)
