from django.conf.urls import url

from calc.views import *

urlpatterns = [
    
    # My home page
    url(r'^submit_new_form/', submit_new_form, name ="submit_new_form"),
    

]
