from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Pacientes
from django.contrib import messages as msg
from django.contrib.messages import constants
from .utils import valida_campos_pacientes


@login_required(login_url="/auth/login")
def pacientes(request):
    if request.method == "GET":
        return render(request, "pacientes.html")
    if request.method == "POST":
        try:
            nome = request.POST.get("nome")
            idade = request.POST.get("idade")
            sexo = request.POST.get("sexo")
            email = request.POST.get("email")
            telefone = request.POST.get("telefone")

            valida_campos_pacientes(
                request,
                nome=nome,
                idade=idade,
                sexo=sexo,
                email=email,
                telefone=telefone,
            )

            msg.add_message(
                request,
                constants.SUCCESS,
                "Paciente cadastrado com sucesso!",
            )
            
            return render(request, "pacientes.html")

        except Exception as error:
            print(f"Houve um error por razoes de : {error}")
