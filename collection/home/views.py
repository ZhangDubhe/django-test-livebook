from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
# Create your views here.
from io import BytesIO
from reportlab.pdfgen import canvas

def index(request):
    return render(request, 'home/index.html',{
        'content':'Hello world',
        'title':'Home'
    })

def document(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="test.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response