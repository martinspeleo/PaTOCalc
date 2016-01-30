from django.conf.urls import url

from pdfviewer.views import *

urlpatterns = [
    
    # Admin home page
    url(r'^pdf/(.*).pdf', make_pdf, name ="pdf_viewer"),
    

]
