from django.shortcuts import render, redirect
from .models import Pacientes
from django.contrib import messages as msg
from django.contrib.messages import constants


def valida_campos_pacientes(request, nome, idade, sexo, email, telefone):

    if (
        (len(nome.strip()) == 0)
        or (len(sexo.strip()) == 0)
        or (len(idade.strip()) == 0)
        or (len(email.strip()) == 0)
        or (len(telefone.strip()) == 0)
    ):
        msg.add_message(request, constants.ERROR, "Preencha todos os campos")
        return redirect("/plataforma/pacientes/")

    if not idade.isnumeric():
        msg.add_message(request, constants.ERROR, "Digite uma idade válida")
        return redirect("/plataforma/pacientes/")

    pacientes = Pacientes.objects.filter(email=email)

    if pacientes.exists():
        msg.add_message(
            request, constants.ERROR, "Já existe um paciente com esse E-mail"
        )
        return redirect("/plataforma/pacientes/")
