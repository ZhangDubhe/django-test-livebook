from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
import datetime
import random
from .models import Disease, DiseaseLink, Symptom

# Create your views here.
def index(request):
    print("request is : ____", request)
    return render(request, 'home/index.html',{
        'content': 'Thanks for giving your time',
        'title':'Quiz or Poll'
    })

def polls(request):
    return render(request, 'polls/index.html',{
        'content':'This is poll page ',
        'title':'Poll'
    })

def quiz(request):
    random_number = 3*random.random()
    try:
        diseases = Disease.objects.all()
    except Disease.DoesNotExist:
        raise Http404("Diseases do not exist")

    try:
        symptoms = Symptom.objects.all()
    except Disease.DoesNotExist:
        raise Http404("Symptoms do not exist")

    return render(request, 'quiz/index.html', {
        'preview': 'This is quiz page',
        'title': 'Quiz',
        'diseases': diseases,
        'symptoms': symptoms,
        'random_number': random_number,
    })

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)