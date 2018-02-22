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
	para = "Today topic is about Otitis (Ear inflammation), there are around three disease in this topic. Now let's challenge."
	return render(request, 'home/index.html', {
		'content': content,
		'title': 'Home',
		'username': user_name,
		'para': para
	})


def get_random():
	return random.uniform(0, 3)


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


def quiz(request, uuid, **topic):
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
	if not topic :
		topic = 'Otitis'

	try:
		disease = Disease.objects.filter(concept_type=topic).order_by('?')[0]
	except:
		disease = "Otitis"

	is_symptom = DiseaseLink.objects.filter(disease_id=disease.id)
	if is_symptom:

		ran = get_random()
		symptom = Symptom.objects.get(id=is_symptom.order_by("?")[0].symptom_id)
		is_property = Property.objects.filter(symptom__id=symptom.id)
		if ran <= 1:
			type = "symptom"
		elif 1 < ran <= 2:
			type = "property"
		elif 2 < ran <= 3:
			if is_property:
				type = "value"
			else:
				type = "property"
	else:
		type = "symptom"

	if type == "symptom":
		if is_symptom:
			try:
				symptoms = []
				for each in is_symptom:
					s_id = each.symptom_id
					symptoms.append(Symptom.objects.get(id=s_id))
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
		s_id = symptom.id
		v_property = Property.objects.filter(symptom__id=s_id).order_by("?")[0]
		try:
			v_values = Value.objects.get(symptom__id=s_id, disease__id=disease.id, property__id=v_property.id)
		except:
			v_values = None
		properties = None
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
		print("="*10)
		print(request.POST.get('data'))
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
				try:
					dl = DiseaseLink.objects.get(disease_id=question_id, symptom_id=each["id"])
					count_a = dl.count_agree
					dl.count_agree = count_a + 1
					dl.save()
					result = "Update log success"
				except:
					dl = DiseaseLink(disease_id=question_id, symptom_id=each["id"], count_agree=1, count_disagree=0,
					                 is_valid=True)
					dl.save()
					result = "Create log success"
			status = 20
		elif type == 'property':
			for each in selections:
				print("id",each["id"],"name", each["text"])
				if each["id"] == "":
					print("[+]creating")
					print("-"*10)
					np = Property(symptom_id=question_id, property_describe=each["text"], count_editor=1)
					np.save()
					result = "Create log Success"
				else:
					rp = Property.objects.get(id=each["id"])
					count = rp.count_editor + 1
					rp.count_editor = count
					rp.save()
					result = "Update log Success"
			status = 20

		elif type == "value":
			disease_id = int(question_id.split("+")[0])
			symptom_id = int(question_id.split("+")[1])
			property_id = int(question_id.split("+")[2])
			for each in selections:
				if each["id"] == "":
					try:
						new_v = Value(disease_id=disease_id, symptom_id=symptom_id, property_id =property_id, count_editor= 1, value_detail=each["text"])
						new_v.save()
						result = "Create value log success"
						status = 20
					except:
						result = "Create Error. Please Try Again"
						status = 0
				else:
					resist_value = Property.objects.get(id=each["id"])
					count = resist_value.count_editor + 1
					resist_value.count_editor = count
					resist_value.save()
					result = "Update value log Success"
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
