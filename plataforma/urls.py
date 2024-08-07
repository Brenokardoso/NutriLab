from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import pacientes

urlpatterns = [
    path("pacientes/", pacientes, name="pacientes"),
]
