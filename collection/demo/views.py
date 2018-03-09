from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.utils import timezone
from django.utils.translation import gettext as _
# Create your views here.
from io import BytesIO
from reportlab.pdfgen import canvas
import json
import random
import time


from .models import Disease, Symptom, DiseaseLink, UMLS_tgt, UMLS_st, User, UserLog, Property, Value, Term
from .Authentication import Authentication as auth

def auth_error(request, result):
	return render(request, 'registration/register.html', {
		'title': 'Register',
		'other': result
	})


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
			return auth_error(request,result)
		if useremail:
			pass
		else:
			useremail = 'null'
		if userpassword:
			pass
		else:
			return auth_error(request,result)



		try:
			is_resist_user = User.objects.get(user_name=username)
			if is_resist_user:
				results = "Already have this name, please input another."
		except User.DoesNotExist:
			try:
				user = User(user_name=username, user_email=useremail, user_password=userpassword, is_admin= False)
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


def get_random():
	return random.uniform(0, 3)


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
		if ran <= 1:
			if ran <= 0.5:
				type = "symptom"
			else:
				type = "symptom-valid"
		elif 1 < ran <= 1.5:
			type = 'property'
		elif 1.5 < ran <= 3:
			is_property = Property.objects.filter(symptom__id=symptom.id)
			if is_property:
				if ran <= 2:
					type = "property-valid"
				else:
					v_property = is_property.order_by('?')[0]
					try:
						val = Value.objects.get(symptom__id=symptom.id, disease__id=disease.id, property__id=v_property.id)
						if 2.5 < ran <= 3:
							type = "value"
						else:
							type = "value-valid"
					except Value.DoesNotExist:
						type = "value"
			else:
				type = "property"
	else:
		type = "symptom"

	duration = time.time() - start_time
	print("[ + ] ================ SENDING ================")
	print("[ + ] type = "+type+" takes " + str(duration))
	print("[ + ] ================ ======= ================")
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
		val = None
	elif type == "symptom-valid":
		symptom = Symptom.objects.get(id=is_symptom.order_by("?")[0].symptom_id)
		properties = None
		symptoms = None
		v_property = None
		v_values = None
		val = None
	elif type == "property":
		symptom = Symptom.objects.get(id=is_symptom.order_by("?")[0].symptom_id)
		try:
			properties = Property.objects.filter(symptom__id=symptom.id)
		except:
			properties = []
		symptoms = None
		v_property = None
		v_values = None
		val = None
	elif type == "property-valid":
		properties = None
		symptoms = None
		v_property = Property.objects.filter(symptom__id=symptom.id)[0]
		v_values = None
		val = None
	elif type == "value":
		s_id = symptom.id
		try:
			v_values = Value.objects.filter(symptom__id=s_id, disease__id=disease.id, property__id=v_property.id)
		except:
			v_values = None
		properties = None
		symptoms = None
		val = None
	elif type == 'value-valid':
		symptom = symptom
		v_property = v_property
		val = val
		properties = None
		symptoms = None
		v_values = None

	defination = Term.objects.get(concept_identifier=disease.content_unique_id).definition
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
		'value': val,
		'defination':defination,
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
		print("[ + ] ",request.POST.get('data'))
		print("[ + ] ================ ====== ================")
		data = json.loads(request.POST.get('data'))

		question_id = data["question_id"]
		selections = data["selections"]
		type = data["type"]
		uuid = data["uuid"]

		if type == 'symptom':
			for each in selections:
				try:
					dl = DiseaseLink.objects.get(disease_id=question_id, symptom_id=each["id"])
					count_a = dl.count_agree
					dl.count_agree = count_a + 1
					dl.save()
					result = "Update log success"
					createLog(uuid=uuid, type=type, item_id=dl.id)
				except:
					dl = DiseaseLink(disease_id=question_id, symptom_id=each["id"], count_agree=1, count_disagree=0,
					                 is_valid=True)
					dl.save()
					result = "Create log success"
					createLog(uuid=uuid, type=type, item_id=dl.id)
			status = 20

		elif type == 'symptom-valid':
			symptom_id = selections
			try:
				dl = DiseaseLink.objects.get(disease_id=question_id, symptom_id=symptom_id)
				is_agree = data["is_agree"]
				count_a = dl.count_agree
				count_da = dl.count_disagree
				if is_agree == 'True':
					count_a = count_a + 1
					print('you agree')
				else:
					count_da = count_da + 1
					print('you disagree')
				dl.is_valid = (False, True)[count_a > count_da]
				dl.count_agree = count_a
				dl.count_disagree = count_da
				dl.save()
				result = "Update log success"
				status = 20
				createLog(uuid=uuid, type=type, item_id=dl.id)
			except DiseaseLink.DoesNotExist:
				result = "Update log failure, Please try again"
				status = 0

		elif type == 'property':
			for each in selections:
				if each["id"] == "" or each["id"] == "undefined" :
					np = Property(symptom_id=question_id, property_describe=each["text"], count_editor=1)
					np.save()
					result = "Create log Success"
					createLog(uuid=uuid, type=type, item_id=np.id)
				else:
					rp = Property.objects.get(id=each["id"])
					count = rp.count_editor + 1
					rp.count_editor = count
					rp.save()
					result = "Update log Success"
					createLog(uuid=uuid, type=type, item_id=rp.id)
			status = 20

		elif type == 'property-valid':
			is_agree = data["is_agree"]
			rp = Property.objects.get(id=selections)

			if is_agree == 'True':
				count = rp.count_editor + 1
				print('you agree')
			else:
				count = rp.count_editor - 1
				print('you disagree')
			rp.count_editor = count
			rp.save()
			result = "Update log Success"
			status = 20
			createLog(uuid=uuid, type=type, item_id=rp.id)

		elif type == "value":
			disease_id = int(question_id.split("+")[0])
			symptom_id = int(question_id.split("+")[1])
			property_id = int(question_id.split("+")[2])
			for each in selections:
				if each["id"] == "" or each["id"] == "undefined" :
					try:
						new_v = Value(disease_id=disease_id, symptom_id=symptom_id, property_id =property_id, count_editor= 1, value_detail=each["text"])
						new_v.save()
						result = "Create value log success"
						status = 20
						createLog(uuid=uuid, type=type, item_id=new_v.id)
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
					createLog(uuid=uuid, type=type, item_id=resist_value.id)

		elif type == "value-valid":
			selection_id = selections
			try:
				resist_value = Property.objects.get(id=selection_id)

				is_agree = data["is_agree"]
				if is_agree == 'True':
					count = resist_value.count_editor + 1
					print('you agree')
				else:
					count = resist_value.count_editor - 1
					print('you disagree')

				resist_value.count_editor = count
				resist_value.save()
				result = "Update value log Success"
				status = 20
				createLog(uuid=uuid, type=type, item_id=resist_value.id)
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
				print(defi)
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
			log = UserLog(user_id=uuid,disease_link_id=item_id)
			log.save()
			print('create log success')
		except UserLog.DoesNotExist:
			print('create log failure')
			pass
	elif 'property' in type:
		try:
			log = UserLog(user_id=uuid,property_id=item_id)
			log.save()
			print('create log success')
		except UserLog.DoesNotExist:
			print('create log failure')
			pass
	elif 'value' in type:
		try:
			log = UserLog(user_id=uuid,value_id=item_id)
			log.save()
			print('create log success')
		except UserLog.DoesNotExist:
			print('create log failure')
			pass

def user_status(request, uuid):
	user_log = UserLog.objects.filter(user=uuid).all()
	user = User.objects.get(id=uuid)
	return render(request, 'home/status.html', {
		'title': 'History',
		'username': user.user_name,
		'user': user,
		'logtable': user_log
	})


