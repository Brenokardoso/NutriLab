from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages as msg
from django.contrib.messages import constants
from .ultils import validando_campos_cadastro, email_html
import re, os
from django.conf import settings


# from django.contrib.auth.decorators import login_required


def cadastro(request):

    if request.user.is_authenticated:
        return HttpResponse(f"Você já está autenticado como o {request.user.username}")

    match (request.method):
        case "GET":
            return render(request, "cadastro.html")

        case "POST":
            try:
                usuario = request.POST.get("usuario")
                email = request.POST.get("email")
                senha = request.POST.get("senha")
                confirmar_senha = request.POST.get("confirmar_senha")

                if validando_campos_cadastro(
                    request, usuario, email, senha, confirmar_senha
                ):

                    usuarios = User.objects.create_user(
                        username=usuario,
                        email=email,
                        password=senha,
                        is_active=False,
                    )
                    usuarios.save()

                    path_template = os.path.join(
                        settings.BASE_DIR,
                        "autenticacao/templates/emails/confirma_cadastro.html",
                    )
                    email_html(
                        path_template,
                        "Cadastro confirmado",
                        [
                            email,
                        ],
                        username=usuario,
                    )

                    msg.add_message(
                        request, constants.SUCCESS, "Usuário cadastrado com sucesso"
                    )
                    return redirect("/auth/login")

            except Exception as error:
                print(f"Não foi possível capturar os dados {error}")

    return render(request, "cadastro.html")


def login(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Você já está autenticado como o {request.user.username}")

    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        try:
            user = request.POST.get("usuario")
            senha = request.POST.get("senha")

            user_auth = authenticate(request, username=user, password=senha)
            # user_login = auth_login(request, user_auth)

            if user_auth:
                msg.add_message(
                    request, constants.SUCCESS, "Usuário logado com sucesso!"
                ),
                return HttpResponse("LOGADO")

            else:
                msg.add_message(
                    request, constants.ERROR, "Não foi possível autênticar o usuário"
                )
                return render(request, "login.html")

        except Exception as error:
            print(f"Houve uma exceção por motivos de {error}")

    return render(request, "login.html")


@login_required
def logout(request):
    try:
        request.user.auth_logout()
    except Exception as error:
        print(f"Houve um erro por : {error}")
