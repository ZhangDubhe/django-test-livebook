from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Count
# Create your views here.
from io import BytesIO
from reportlab.pdfgen import canvas
import json
import random
import time

from .models import Disease, Symptom, DiseaseLink, UMLS_tgt, UMLS_st, User, UserLog, Property, Value, Term, Question
from .Authentication import Authentication as auth
from .tables import SimpleTable

MAX_PRIORITY = 10000

def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)


def get_random():
    return random.uniform(0, 3)


def auth_error(request, result):
    return render(request, 'registration/register.html', {
        'title': 'Register',
        'other': result
    })


def queueQuestion(topic):
    firstTry = Question.objects.filter(topic=topic).order_by('-priority')[0]
    question = Question.objects.filter(topic=topic, priority=firstTry.priority).order_by("?")[0]
    # 10 - 10000
    # After upload: minus 10
    # Bigger in numeric has high priority
    # New question
    return question


def createQuestion(topic, type, head_id, body_id, disease_id):
    global MAX_PRIORITY
    if type == "symptom-valid":
        head = Disease.objects.get(id=head_id).name
        body = Symptom.objects.get(id=body_id).symptom_name
    elif type == "property":
        head = Symptom.objects.get(id=head_id).symptom_name
    elif type == "property-valid":
        head = Symptom.objects.get(id=head_id).symptom_name
        body = Property.objects.get(id=body_id).property_describe
    elif type == "value":
        head = Property.objects.get(id=head_id).property_describe
    elif type == "value-valid":
        head = Property.objects.get(id=head_id).property_describe
        body = Value.objects.get(id=body_id).value_detail
    if 'valid' in type:
        try:
            question = Question(topic=topic, type=type, body=body, bodykey=body_id, head=head, headkey=head_id, priority=MAX_PRIORITY, disease=disease_id)
            question.save()
            return 0
        except Question.DoesNotExist:
            print("Error in create question")
        except:
            print(Question(topic=topic, type=type, body=body, body_id=body_id, head=head, head_id=head_id, priority=MAX_PRIORITY, disease=disease_id))
            print("[ error - Valid ]")
    else:
        try:
            question = Question(topic=topic, type=type, head=head, head_id=head_id, priority=MAX_PRIORITY-10,disease=disease_id)
            question.save()
            return 0
        except Question.DoesNotExist:
            print("[ error ]")


def updateQuestion(topic, type, question_id):
    this_question = Question.objects.get(id=question_id)
    if 'valid' in type:
        this_question.priority -= 10
    else:
        this_question.priority -= 50
    this_question.save()
    return 0


def highPriorityQuestion(topic, type, question_id):
    this_question = Question.objects.get(id=question_id)
    this_question.priority = 10000
    this_question.save()
    return 0


def verify_count(count_a, count_da):
    if count_da == 0:
        if count_a > 5:
            return True
        else:
            return False
    else:
        if (count_a / count_da) >= 5:
            return True
        else:
            return False


def register(request):
    status = 0
    if request.method == "POST":
        username = request.POST.get('username')
        useremail = request.POST.get('email')
        userpassword = request.POST.get('password')

        result = 'Information not complete'
        if username:
            pass
        else:
            return auth_error(request, result)
        if useremail:
            pass
        else:
            useremail = 'null'
        if userpassword:
            pass
        else:
            return auth_error(request, result)

        try:
            is_resist_user = User.objects.get(user_name=username)
            if is_resist_user:
                results = "Already have this name, please input another."
        except User.DoesNotExist:
            try:
                user = User(user_name=username, user_email=useremail, user_password=userpassword, is_admin=False)
                user.save()
                results = "Welcome!"
                status = 20
            except:
                results = "Create user error"

    if status == 20:
        user_name = _(user.user_name)
        content = "Are you ready?"
        para = "Today topic is about Otitis (Ear inflammation), there are around three disease in this topic. Now let's challenge."
        return render(request, 'home/index.html', {
            'content': content,
            'title': 'Home',
            'username': user_name,
            'user': user,
            'para': para
        })
    else:
        return render(request, 'registration/register.html', {
            'title': 'Register',
            'other': results
        })


def login(request):
    status = 0
    if request.method == "POST":
        try:
            m = User.objects.get(user_name=request.POST.get('username'))
            if m.user_password == request.POST.get('password'):
                msg = "You're logged in."
                status = 20
            else:
                msg = "Wrong password"
        except User.DoesNotExist:
            msg = "Wrong user name, please register!"

    else:
        msg = "Wrong request"
    if status == 20:
        user_name = _(m.user_name)
        content = "Are you ready?"
        para = "Today topic is about Otitis (Ear inflammation), there are around three disease in this topic. Now let's challenge."
        return render(request, 'home/index.html', {
            'content': content,
            'title': 'Home',
            'username': user_name,
            'user': m,
            'para': para
        })
    else:
        return render(request, 'registration/login.html', {
            'title': 'Login',
            'other': msg
        })


def logout(request):
    return render(request, 'registration/logout.html', {

    })


def password_change(request):
    return render(request, 'registration/logout.html', {

    })


def init_login(request):
    return render(request, 'registration/login.html', {
        'title': 'Login'
    })


def init_register(request):
    return render(request, 'registration/register.html', {
        'title': 'Register'
    })


def index(request):
    user_name = _("user")
    content = "Are you ready?"
    para = "Today topic is about Otitis (Ear inflammation), there are around three disease in this topic. Now let's challenge."
    return render(request, 'home/index.html', {
        'content': content,
        'title': 'Home',
        'username': user_name,
        'para': para
    })


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
    start_time = time.time()
    # check uuid
    try:
        user = User.objects.get(pk=uuid)
    except User.DoesNotExist:
        return render(request, 'home/index.html', {
            'content': "No this user",
            'title': 'Auth Error',
            'username': "no auth"
        })

    para = "You might want to search the term below?"
    user_name = _(user.user_name)
    topic = request.session.get('topic')
    if not topic:
        topic = 'Otitis'
    question = queueQuestion(topic)
    request.session['topic'] = topic
    request.session['question'] = question.id
    type = question.type
    duration = time.time() - start_time
    print("[ + ] ================ SENDING ================")
    print("[ + ] type = " + type + " takes " + str(duration))
    print("[ + ] ================ ======= ================")
    if type == "symptom":
        disease = Disease.objects.get(id=question.headkey)
        is_symptom = DiseaseLink.objects.filter(disease__id=disease.id)
        if is_symptom:
            try:
                symptoms = []
                for each in is_symptom:
                    s_id = each.symptom_id
                    symptoms.append(Symptom.objects.get(id=s_id))
            except Symptom.DoesNotExist:
                pass
        else:
            symptoms = None
        properties = None
        symptom = None
        v_property = None
        v_values = None
        val = None
        defi = disease
    elif type == "symptom-valid":
        disease = Disease.objects.get(id=question.headkey)
        symptom = Symptom.objects.get(id=question.bodykey)
        defi = disease
        properties = None
        symptoms = None
        v_property = None
        v_values = None
        val = None
    elif type == "property":
        symptom = Symptom.objects.get(id=question.headkey)
        try:
            properties = Property.objects.filter(symptom__id=question.headkey)
        except:
            properties = []
        symptoms = None
        v_property = None
        v_values = None
        val = None
        defi = symptom
    elif type == "property-valid":
        symptom = Symptom.objects.get(id=question.headkey)
        v_property = Property.objects.get(id=question.bodykey)
        defi = symptom
        properties = None
        symptoms = None
        v_values = None
        val = None
    elif type == "value":
        disease = Disease.objects.get(id=question.disease)
        v_property = Property.objects.get(id=question.headkey)
        s_id = v_property.symptom
        print("---symptom id", s_id)
        symptom = Symptom.objects.get(id=s_id)
        try:
            v_values = Value.objects.filter(symptom__id=s_id, disease__id=disease.id, property__id=v_property.id)
        except:
            v_values = None
        properties = None
        symptoms = None
        val = None
        defi = disease
    elif type == 'value-valid':
        disease = Disease.objects.get(id=question.disease)
        s_id = v_property.symptom
        print("---symptom id", s_id)
        symptom = Symptom.objects.get(id=s_id)
        v_property = Property.objects.get(id=question.headkey)
        val = Value.objects.get(id=question.bodykey)
        properties = None
        symptoms = None
        v_values = None
        defi = disease

    defination = Term.objects.get(concept_identifier=defi.content_unique_id).definition
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
        'random_int': random_int(1, 10),
        'disease': disease,
        'symptoms': symptoms,
        'symptom': symptom,
        'properties': properties,
        'property': v_property,
        'values': v_values,
        'value': val,
        'defination': defination,
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
        print("[ + ] ================ UPLOAD ================")
        print("[ + ] ", request.POST.get('data'))
        print("[ + ] ================ ====== ================")
        data = json.loads(request.POST.get('data'))

        question_id = data["question_id"]
        selections = data["selections"]
        type = data["type"]
        uuid = data["uuid"]
        topic = request.session.get('topic')
        questionModelId = request.session.get('question')
        # make a flow
        print("[update question]", topic, str(questionModelId))
        if type == 'symptom':
            for each in selections:
                try:
                    dl = DiseaseLink.objects.get(disease_id=question_id, symptom_id=each["id"])
                    dl.is_valid = verify_count(dl.count_agree + 1, dl.count_disagree)
                    dl.count_agree = dl.count_agree + 1
                    dl.save()
                    result = "Update log success"
                    createLog(uuid=uuid, type=type, item_id=dl.id)
                except:
                    try:
                        dl = DiseaseLink(disease_id=question_id, symptom_id=each["id"], count_agree=1, count_disagree=0,
                                         is_valid=False)
                        dl.save()
                        result = "Create  log success"
                        createLog(uuid=uuid, type=type, item_id=dl.id)
                        symptomId = each["id"]
                    except:
                        symptom = Symptom(symptom_name=each["text"], type="Sign or Symptom")
                        symptom.save()
                        dl = DiseaseLink(disease_id=question_id, symptom_id=symptom.id, count_agree=1, count_disagree=0,
                                         is_valid=False)
                        dl.save()
                        result = "Create new symptom log success"
                        createLog(uuid=uuid, type=type, item_id=dl.id)
                        symptomId = symptom.id

                    print("Create new symptom question.")
                    createQuestion(topic=topic, type="symptom-valid", head_id=question_id, body_id=symptomId, disease_id=question_id)

            print("Update disease question.")
            updateQuestion(topic, type, questionModelId)
            status = 20

        elif type == 'symptom-valid':
            symptom_id = selections
            try:
                dl = DiseaseLink.objects.get(disease_id=question_id, symptom_id=symptom_id)
                if data["is_agree"] == 'True':
                    dl.is_valid = verify_count(dl.count_agree + 1, dl.count_disagree)
                    dl.count_agree = dl.count_agree + 1
                    print('you agree')
                else:
                    dl.is_valid = verify_count(dl.count_agree, dl.count_disagree + 1)
                    dl.count_disagree = dl.count_disagree + 1
                    print('you disagree')
                dl.save()
                result = "Update log success"
                status = 20
                createLog(uuid=uuid, type=type, item_id=dl.id)
                if abs(dl.count_agree - dl.count_agree) <= 2:
                    print("Reset symptom verify question.")
                    highPriorityQuestion(topic, type, questionModelId)
                else:
                    print("Update symptom verify question.")
                    updateQuestion(topic, type, questionModelId)
            except DiseaseLink.DoesNotExist:
                result = "Update log failure, Please try again"
                status = 0


        elif type == 'property':
            for each in selections:
                if each["id"] == "" or each["id"] == "undefined":
                    np = Property(symptom_id=question_id, property_describe=each["text"], count_disagree=0,
                                  count_agree=1, is_valid=False)
                    np.save()
                    result = "Create log Success"
                    createLog(uuid=uuid, type=type, item_id=np.id)
                    propertyId = np.id
                else:
                    rp = Property.objects.get(id=each["id"])
                    rp.is_valid = verify_count(rp.count_agree + 1, rp.count_disagree)
                    rp.count_agree = rp.count_agree + 1
                    rp.save()
                    result = "Update log Success"
                    createLog(uuid=uuid, type=type, item_id=rp.id)
                    propertyId = rp.id

                print("Create new property question.")
                createQuestion(topic=topic, type="property-valid", head_id=question_id, body_id=propertyId, disease_id=null)

            status = 20

            print("Update symptom property question.")
            updateQuestion(topic, type, questionModelId)

        elif type == 'property-valid':
            is_agree = data["is_agree"]
            rp = Property.objects.get(id=selections)
            if data["is_agree"] == 'True':
                rp.is_valid = verify_count(rp.count_agree + 1, rp.count_disagree)
                rp.count_agree = rp.count_agree + 1
                print('you agree')
            else:
                rp.is_valid = verify_count(rp.count_agree, rp.count_disagree + 1)
                rp.count_disagree = rp.count_disagree + 1
                print('you disagree')
            rp.save()
            result = "Update log Success"
            status = 20
            createLog(uuid=uuid, type=type, item_id=rp.id)
            if abs(rp.count_agree - rp.count_agree) <= 2:
                print("Reset property verify question.")
                highPriorityQuestion(topic, type, questionModelId)
            else:
                print("Update property verify question.")
                updateQuestion(topic, type, questionModelId)

        elif type == "value":
            disease_id = int(question_id.split("+")[0])
            symptom_id = int(question_id.split("+")[1])
            property_id = int(question_id.split("+")[2])
            for each in selections:
                if each["id"] == "" or each["id"] == "undefined":
                    try:
                        new_v = Value(disease_id=disease_id, symptom_id=symptom_id, property_id=property_id,
                                      count_disagree=0, count_agree=1, is_valid=False, value_detail=each["text"])
                        new_v.save()
                        result = "Create value log success"
                        status = 20
                        createLog(uuid=uuid, type=type, item_id=new_v.id)
                        print("Create new value question.")
                        createQuestion(topic=topic, type="value-valid", head_id=property_id, body_id=new_v.id, disease_id=disease_id)
                    except:
                        result = "Create Error. Please Try Again"
                        status = 0
                else:
                    resist_value = Value.objects.get(id=each["id"])
                    resist_value.is_valid = verify_count(resist_value.count_agree + 1, resist_value.count_disagree)
                    resist_value.count_agree = resist_value.count_agree + 1
                    resist_value.save()
                    result = "Update value log Success"
                    status = 20
                    createLog(uuid=uuid, type=type, item_id=resist_value.id)
                    valueId = resist_value.id
                    print("Create new value question.")
                    createQuestion(topic=topic, type="value-valid", head_id=property_id, body_id=valueId, disease_id=disease_id)

            print("Update  property value question.")
            updateQuestion(topic, "value", questionModelId)

        elif type == "value-valid":
            selection_id = selections
            try:
                resist_value = Property.objects.get(id=selection_id)
                if data["is_agree"] == 'True':
                    resist_value.is_valid = verify_count(resist_value.count_agree + 1, resist_value.count_disagree)
                    resist_value.count_agree = resist_value.count_agree + 1
                    print('you agree')
                else:
                    resist_value.is_valid = verify_count(resist_value.count_agree, resist_value.count_disagree + 1)
                    resist_value.count_disagree = resist_value.count_disagree + 1
                    print('you disagree')
                resist_value.save()
                result = "Update value log Success"
                status = 20
                createLog(uuid=uuid, type=type, item_id=resist_value.id)
                if abs(resist_value.count_agree - resist_value.count_agree) <= 2:
                    print("Reset symptom verify question.")
                    highPriorityQuestion(topic, type, questionModelId)
                else:
                    print("Update value verify question.")
                    updateQuestion(topic, "value-valid", questionModelId)

            except Property.DoesNotExist:
                status = 0
                result = "updating value log error"
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


def search_terms(request):
    if request.method == "GET":
        type = request.GET.get("type")
        str = request.GET.get("str")
        status = 200

        if type == "symptom":
            res_list = []
            results = Symptom.objects.filter(symptom_name__contains=str)
            for each in results:
                res = {}
                defi = Term.objects.filter(concept_identifier=each.content_unique_id)[0]
                print("[Term]",defi.name)
                res["name"] = each.symptom_name
                res["id"] = each.id
                res["source"] = defi.source
                res["def"] = defi.definition
                res["cui"] = defi.concept_identifier
                res["type"] = defi.semantic_type
                res_list.append(res)
            results = res_list
        elif type == "value":
            results = "Input to add"
            status = 0
        else:
            results = Term.objects.filter(name__contains=str)
            res_list = []
            for each in results:
                res = {}
                res["name"] = each.name
                res["source"] = each.source
                res["def"] = each.definition
                res["cui"] = each.concept_identifier
                res["type"] = each.semantic_type
                res["id"] = ''
                res_list.append(res)
            results = res_list
        return HttpResponse(json.dumps({
            "results": results,
            "status": status
        }))


def search_self(request):
    if request.method == "GET":
        type = request.GET.get("type")
        str = request.GET.get("str")

        status = 200
        if type == "symptom":
            res_list = []
            results = Symptom.objects.filter(symptom_name__contains=str)
            for each in results:
                res = {}
                res["name"] = each.symptom_name
                res["id"] = each.id
                res_list.append(res)
            results = res_list

        elif type == "property":
            res_list = []
            results = Property.objects.filter(property_describe__contains=str)
            for each in results:
                res = {}
                res["name"] = each.property_describe
                res["id"] = each.id
                res_list.append(res)
            results = res_list
        elif type == "value":
            res_list = []
            results = Value.objects.filter(value_detail__contains=str)
            for each in results:
                res = {}
                res["name"] = each.value_detail
                res["id"] = each.id
                res_list.append(res)
            results = res_list
        else:
            results = "Wrong type in request."
            status = 0
        return HttpResponse(json.dumps({
            "results": results,
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


def createLog(uuid, type, item_id):
    print("Creating log---")
    if 'symptom' in type:
        try:
            log = UserLog(user_id=uuid, disease_link_id=item_id)
            log.save()
            print('create log success')
        except UserLog.DoesNotExist:
            print('create log failure')
            pass
    elif 'property' in type:
        try:
            log = UserLog(user_id=uuid, property_id=item_id)
            log.save()
            print('create log success')
        except UserLog.DoesNotExist:
            print('create log failure')
            pass
    elif 'value' in type:
        try:
            log = UserLog(user_id=uuid, value_id=item_id)
            log.save()
            print('create log success')
        except UserLog.DoesNotExist:
            print('create log failure')
            pass


def user_status(request, uuid):
    user_log = UserLog.objects.filter(user=uuid).all()
    try:
        count = user_log.values('user').annotate(tol=Count('id')).order_by('tol')[0]["tol"]
    except:
        count = '0'
    print("[+] history count:", count)
    user = User.objects.get(id=uuid)

    user_log = SimpleTable(user_log)
    return render(request, 'home/status.html', {
        'title': 'History',
        'username': user.user_name,
        'user': user,
        'logtable': user_log,
        'count': count
    })
