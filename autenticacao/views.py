from django.shortcuts import render, redirect, get_object_or_404
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
from .models import Ativacao
from hashlib import sha256


def cadastro(request):

    if request.user.is_authenticated:
        return redirect("/plataforma/pacientes")

    match (request.method):
        case "GET":
            return render(request, "cadastro.html")

        case "POST":
            try:
                usuario = request.POST.get("usuario")
                email = request.POST.get("email")
                senha = request.POST.get("senha")
                confirmar_senha = request.POST.get("confirmar_senha")
                host = request.get_host()

                if validando_campos_cadastro(
                    request, usuario, email, senha, confirmar_senha
                ):

                    user = User.objects.create_user(
                        username=usuario,
                        email=email,
                        password=senha,
                        is_active=False,
                    )
                    token = sha256(f"{usuario}{email}{senha}".encode()).hexdigest()
                    ativacao = Ativacao(
                        token=token,
                        user=user,
                    )
                    ativacao.save()
                    user.save()

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
                        link_ativacao=f"{host}/auth/ativar_conta/{token}",
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
        return redirect("/plataforma/pacientes")

    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        try:
            user = request.POST.get("usuario")
            senha = request.POST.get("senha")

            user_auth = authenticate(request, username=user, password=senha)

            if user_auth:
                auth_login(request, user_auth)
                return redirect("/plataforma/pacientes")

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
        return HttpResponse("Usuário deslogado!")
    except Exception as error:
        print(f"Houve um erro por : {error}")


def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        msg.add_message(request, constants.WARNING, "Este token já existe")
        return redirect("/auth/login")
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    token.ativo = True
    user.save()
    token.save()

    msg.add_message(request, constants.SUCCESS, "Usuário ativado com sucesso")
    return redirect("/auth/login")
