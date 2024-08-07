from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .views import *

urlpatterns = [
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login, name="login"),
    path("sair", logout, name="sair"),
    path("ativar_conta/<str:token>", ativar_conta, name="ativar_conta"),
]
