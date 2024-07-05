from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages as msg
from django.contrib.messages import constants
from .ultils import validando_campos
import re

# from django.contrib.auth.decorators import login_required


def cadastro(request):

    match (request.method):
        case "GET":
            return render(request, "cadastro.html")

        case "POST":
            try:
                usuario = request.POST.get("usuario")
                email = request.POST.get("email")
                senha = request.POST.get("senha")
                confirmar_senha = request.POST.get("confirmar_senha")

                if validando_campos(request, usuario, email, senha, confirmar_senha):

                    usuarios = User.objects.create_user(
                        username=usuario,
                        email=email,
                        password=senha,
                        is_active=False,
                    )
                    usuarios.save()

                    msg.add_message(
                        request,
                        constants.SUCCESS,
                        "Usuário cadastrado com sucesso",
                    )

                    print("Usuário cadastrado com sucesso")

                    return render(request, "cadastro.html")

            except Exception as error:
                print(f"Não foi possível capturar os dados {error}")

    return render(request, "cadastro.html")


def login(request):
    return render(request, "login.html")
