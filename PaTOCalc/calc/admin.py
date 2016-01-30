from django.contrib import admin

from calc.models import FormGenerator, FormInstance

class ReneratedForms(admin.ModelAdmin):
    pass
    
class FormInstanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(FormGenerator, ReneratedForms)
admin.site.register(FormInstance, FormInstanceAdmin)
