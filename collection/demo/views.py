from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.utils import timezone
from django.utils.translation import gettext as _
# Create your views here.
from io import BytesIO
from reportlab.pdfgen import canvas
import json
import random

from .models import Disease, Symptom, DiseaseLink, UMLS_tgt, UMLS_st, User, UserLog, Property, Value
from .Authentication import Authentication as auth


def index(request):
    user_name = _("user")
    content = "Are you ready?"
    para = "Please read this carefully."
    return render(request, 'home/index.html', {
        'content': content,
        'title': 'Home',
        'username': user_name,
        'para': para
    })


def get_random():
    return random.uniform(0,3)


#   1,2,3,4


def user_auth(uuid):
    try:
        user_is_related = User.objects.get(pk=uuid).is_related
    except User.DoesNotExist:
        return False
    if user_is_related:
        return True
    else:
        return False


def quiz(request, uuid):
    # check uuid
    try:
        user = User.objects.get(pk=uuid)
        if user.is_doctor:
            pass
        else:
            return render(request, 'home/index.html', {
                'content': "Your have no such permission",
                'title': 'Auth Error',
                'username': user.user_name
            })
    except User.DoesNotExist:
        return render(request, 'home/index.html', {
            'content': "No this user",
            'title': 'Auth Error',
            'username': "no auth"
        })

    para = "You might want to search the term below?"
    user_name = _(user.user_name)

    try:
        disease = Disease.objects.filter(concept_type='Otitis').order_by('?')[0]
    except:
        disease = "Otitis"

    is_symptom = DiseaseLink.objects.filter(disease_id=disease.id)
    if is_symptom:
        ran = get_random()
        if ran <= 1:
            type = "symptom"
        elif 1 < ran <= 2:
            type = "property"
        elif 2 < ran <= 3:
            type = "value"
    else:
        type = "symptom"

    if type == "symptom":
        if is_symptom:
            try:
                symptoms = []
                for each in is_symptom:
                    s_id = each.symptom_id
                    symptoms.append(Symptom.objects.get(id=s_id))

            # TODO:     to query which have link with the disease
            except Symptom.DoesNotExist:
                raise Http404("Symptoms do not exist")
        else:
            symptoms = None
        properties = None
        symptom = None
        v_property = None
        v_values = None

    elif type == "property":
        symptom = Symptom.objects.get(id=is_symptom.order_by("?")[0].symptom_id)
        try:
            properties = Property.objects.filter(symptom__id=symptom.id)
        except:
	        properties = []

        symptoms = None
        v_property = None
        v_values = None

    elif type == "value":
        s_id = is_symptom.order_by("?")[0].symptom_id
        p_id = Value.objects.filter(symptom__id=s_id, disease__id=disease.id)
        v_property = Property.objects.get(id=p_id)
        v_values = None
        properties = None
        symptom = None
        symptoms = None

    #  query Tgt
    try:
        tgt = UMLS_tgt.objects.order_by('-add_at')[0]
        if not is_tgt_valid(tgt):
            tgt = create_new_tgt()
    except:
        tgt = create_new_tgt()
    return render(request, 'quiz/index.html', {
        'title': 'Home',
        'username': user_name,
        'user': user,
        'para': para,
        'type': type,
        'disease': disease,
        'symptoms': symptoms,
        'symptom': symptom,
        'properties': properties,
        'property': v_property,
        'values': v_values,
        'tgt': tgt
    })


def polls(request):
    return render(request, 'polls/index.html', {
        'content': 'This is poll page ',
        'title': 'Poll'
    })


def update_disease(request):
    if request.method == "POST":
        name = request.POST.get('name')
        cui = request.POST.get('cui')
        try:
            Disease.objects.create(name=name, content_unique_id=cui)
            result = "UPDATE Disease success"
            status = 20
        except:
            result = "UPDATE Disease error"
            status = 500
        return HttpResponse(json.dumps({
            "result": result,
            "status": status
        }))


def upload_answer(request):
    if request.method == 'POST' and request.POST.get('name') == 'answer':

        data = json.loads(request.POST.get('data'))

        # data.question_id = $(".question-head")[0].id.split("_")[1];
        # data.selections = select_info;
        # {ans.id , ans.text};
        # data.type = type;
        question_id = data["question_id"]
        selections = data["selections"]
        type = data["type"]
        if type == 'symptom':
            for each in selections:
                print(each["id"], each["text"])
                symptom = Symptom.objects.get(content_unique_id=each["id"])
                try:
                    dl = DiseaseLink.objects.get(disease_id=question_id, symptom_id=symptom.id)
                    count_a = dl.count_agree
                    dl.count_agree = count_a + 1
                    dl.save()
                    result = "Update log success"
                except:
                    dl = DiseaseLink(disease_id=question_id, symptom_id=symptom.id, count_agree=1, count_disagree=0,
                                     is_valid=True)
                    dl.save()
                    result = "Create log success"

            status = 20
        else:
            status = 0
            result = "updating database error"

    else:
        status = 0
        result = "get data error"

    return HttpResponse(json.dumps({
        "result": result,
        "status": status
    }))


def add_symptom(request):
    if request.method == "POST":
        name = request.POST.get('name')
        cui = request.POST.get('cui')
        try:
            Symptom.objects.create(name=name, content_unique_id=cui)
            result = "UPDATE Symptom success"
            status = 20
        except:
            result = "UPDATE Symptom error"
            status = 500
        return HttpResponse(json.dumps({
            "result": result,
            "status": status
        }))


def update_disease_link(disease_id, symptom_id):
    try:
        result = DiseaseLink.objects.filter(disease_id=disease_id, symptom_id=symptom_id)
    except:
        result = "UPDATE Symptom success"
        status = 20

    return result;


def umls_auth(request):
    if request.method == "POST":
        name = request.POST.get('name')
        status = 0
        if name:
            try:
                tgt_res = UMLS_tgt.objects.order_by('-add_at')[0]
            except:
                tgt_res = None

            if tgt_res != None:
                if is_tgt_valid(tgt_res):
                    pass
                else:
                    tgt_res = create_new_tgt()
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
            "tgt": str(tgt_res)
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
