from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('account/login', views.initLogin, name="login"),
    path('account/login-post', views.login, name="login-post"),
    path('account/login-post/<int:uuid>/', views.login, name="login-post-reload"),
    path('account/register', views.initRegister, name="register"),
    path('account/register-post', views.register, name="register-post"),
    path('account/logout', views.logout, name="logout"),
    path('account/logouted', views.logout, name="logouted"),
    path('account/psw', views.changePassword, name="psw"),
    path('document', views.document, name='docs'),
    path('status/u/<int:uuid>/', views.showUserStatus, name='status'),
    path('demo', views.quiz, name='demo'),
    path('umls-auth', views.umls_auth, name='umls-auth'),
    path('upload-answer', views.uploadAnswer, name='upload-answer'),
    path('search-terms', views.searchTerms, name='search-terms'),
    path('quiz/disease/<int:uuid>/', views.quiz, name='quiz')
    # path('polls', views.polls, name='polls'),
]