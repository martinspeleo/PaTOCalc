from django.conf.urls import url

from .views import *

urlpatterns = [
    
    # Admin home page
    url(r'^admin_home_page/', admin_home_page, name ="admin_home_page"),
    url(r'^submit_new_form/', submit_new_form, name ="submit_new_form"),
    url(r'^new_form_instance/([^/]*)/([^/]*)', new_form_instance, name ="new_form_instance"),
    url(r'^evaluate/([^/]*)/([^/]*)', evaluate, name ="evaluate"),
    url(r'^generators/', CalculatorListView.as_view(), name="choose-generator")
    
    # Patients' Authorized Forms
    #url(r'^patient_demographic/(?P<mrn>\.+)', patient_demographic, name ="patient_demographic"),

    
]
