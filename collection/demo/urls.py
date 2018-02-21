from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('document', views.document, name='docs'),
    path('demo', views.quiz, name='demo'),
    path('umls-auth', views.umls_auth , name='umls-auth'),
    path('upload-answer', views.upload_answer , name='upload-answer'),
    path('search-terms', views.search_terms , name='search-terms'),
    path('quiz/disease/<int:uuid>/', views.quiz, name='quiz')
    # path('polls', views.polls, name='polls'),
]