from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
# Create your views here.
from io import BytesIO
from reportlab.pdfgen import canvas
from .models import UMLS_tgt, UMLS_st
# from ..newhub.models import Disease, Symptom, DiseaseLink

import json
from  .Authentication import Authentication as auth
from django.utils import timezone

def index(request):
    return render(request, 'home/index.html', {
        'content': 'Please input the name of disease:',
        'title': 'Home'
    })
#
# def quiz(request):
#     try:
#         diseases = Disease.objects.all()
#     except Disease.DoesNotExist:
#         raise Http404("Diseases do not exist")
#
#     try:
#         symptoms = Symptom.objects.all()
#     except Disease.DoesNotExist:
#         raise Http404("Symptoms do not exist")
#
#     return render(request, 'quiz/index.html', {
#         'preview': 'This is quiz page',
#         'title': 'Quiz',
#         'diseases': diseases,
#         'symptoms': symptoms
#     })

def umls_auth(request):
    if request.method == "POST":
        name = request.POST.get('name')
        status = 0
        if name:
            tgt_res = UMLS_tgt.objects.order_by('-add_at')[0]
            if is_tgt_valid(tgt_res):
                pass
            else:
                tgt_res = create_new_tgt()
            st = create_new_st(tgt_res)
            if st:
                result = str(st)
                status = 200
        else:
            result = "Please INPUT something"
        print(result)
        return HttpResponse(json.dumps({
            "status": status,
            "result": result,
            "tgt": str(tgt_res),
            "tgt_exp": UMLS_tgt.objects.order_by('-add_at')[0].add_at.timestamp() + 28800
        }))

def is_tgt_valid(tgt):
    now_time = timezone.now().timestamp()
    add_time = tgt.add_at.timestamp()
    during = now_time - add_time
    # valid 8 hours
    if during >= 28800:
        return False
    else:
        return True

def create_new_st(tgt):
    connect = auth()
    st = None
    try:
        st = connect.getst(tgt)
    except:
        return False
    if st:
        try:
            UMLS_st.objects.create(ticket=st)
            return st
        except:
            return False

def create_new_tgt():
    connect = auth()
    tgt = None
    try:
        tgt = connect.gettgt()
    except:
        return False
    if tgt:
        try:
            UMLS_tgt.objects.create(ticket=tgt)
            return tgt
        except:
            return False



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
