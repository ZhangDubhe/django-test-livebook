from django.test import TestCase
from .models import Disease, Question
# Create your tests here.


class QuestionTest():

	def generateDefaultQuestion(self):
		lastestQuestion = ''
		try:
			questions = Question.objects.filter(type='symptom')
			lastestQuestion = questions.order_by('-add_at')[0]
		except:
			print("not have questions yet")
		if lastestQuestion != '':
			try:
				diseases = Disease.objects.filter(id__gt=lastestQuestion.headkey)
			except Disease.DoesNotExist:
				return 0
		else:
			diseases = Disease.objects.all()
		for each in diseases:
			new = Question(topic=each.concept_type, type='symptom', head=each.name, headkey=each.id, priority=10000-10)
			new.save()
		return 1