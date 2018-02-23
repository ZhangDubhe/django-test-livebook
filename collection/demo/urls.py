from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('account/login', views.init_login, name="login"),
    path('account/login-post', views.login, name="login-post"),
    path('account/register',views.init_register, name="register"),
    path('account/register-post',views.register, name="register-post"),
    path('account/logout', views.logout, name="logout"),
    path('account/logouted', views.logout, name="logouted"),
    path('account/psw', views.password_change, name="psw"),
    path('document', views.document, name='docs'),
    path('demo', views.quiz, name='demo'),
    path('umls-auth', views.umls_auth , name='umls-auth'),
    path('upload-answer', views.upload_answer , name='upload-answer'),
    path('search-terms', views.search_terms , name='search-terms'),
    path('quiz/disease/<int:uuid>/', views.quiz, name='quiz')
    # path('polls', views.polls, name='polls'),
]