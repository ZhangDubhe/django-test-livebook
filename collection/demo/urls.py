from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('document', views.document, name='docs'),
    path('demo', views.quiz, name='demo'),
    path('umls_auth', views.umls_auth , name='umls_auth'),
    path('quiz/disease/<int:uuid>/', views.quiz, name='quiz'),
    path('next_quiz', views.quiz, name='next')
    # path('polls', views.polls, name='polls'),
]