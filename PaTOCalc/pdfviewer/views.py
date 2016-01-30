#from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from calc.models import FormInstance

@login_required
def make_pdf(request, fi_pk):
    fi = get_object_or_404(FormInstance, pk = fi_pk)
    form_data = fi.get_data()
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    y = 100
    
    for key, value in form_data.iteritems():
        p.drawString(100, y, unicode(key))
        p.drawString(300, y, unicode(value))
        y = y - 10

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

#def displayoutput():
#    tf = tempfile.NamedTemporaryFile(delete=False)
#    body = """
#    <html>
#      <head>
#        <meta name="pdfkit-page-size" content="Legal"/>
#        <meta name="pdfkit-orientation" content="Landscape"/>
#      </head>
 #     Hello World!
#      </html>
#    """
#    print tf.name
#    pdfkit.from_string(body, tf.name) #with --page-size=Legal and --orientation=Landscape
    
