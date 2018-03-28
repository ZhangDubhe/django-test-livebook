import django_tables2 as tables
from django_tables2 import A
import itertools
from .models import UserLog, DiseaseLink, Disease, Symptom, Value

class SimpleTable(tables.Table):
	# ('id', 'user', 'get_disease_name', 'get_symptom_name', 'get_property', 'value', 'add_at')

	id = tables.Column()
	disease = tables.Column(empty_values=())
	property = tables.Column(empty_values=())
	symptom = tables.Column(empty_values=(), verbose_name="Symptom")

	def render_property(self, record):
		try:
			name = record.value.property
		except:
			try:
				name = record.property
			except:
				name = '—'
		if name != None:
			return name
		else:
			return "—"

	def render_symptom(self, record):
		# print("[Disease link]", record.disease_link)
		if record.disease_link != None:
			if record.disease_link.symptom != None:
				return str(record.disease_link.symptom)
		else:
			if record.property != None:
				return str(record.property.symptom)
			else:
				if record.value != None:
					return str(record.value.symptom)


	def render_disease(self, record):
		# print("[Disease link]", record.disease_link)
		try:
			name = record.disease_link.disease
		except:
			try:
				name = record.value.disease
			except:
				name = '—'
		return name


	class Meta:
		model = UserLog
		fields = ('id', 'disease', 'symptom', 'property', 'value', 'add_at')