#from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from calc.models import FormInstance

def make_pdf(request, fi_pk):
    fi = get_object_or_404(FormInstance, pk = fi_pk)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")
    p.drawString(300, 100, "Hello world.")

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
    