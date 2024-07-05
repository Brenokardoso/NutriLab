from django.contrib.auth.models import User
import re
from django.contrib.messages import constants
from django.contrib import messages as msg
from django.db.models import Q


def validando_campos(request, usuario, email, senha, confirmar_senha):

    fields = [usuario, email, senha, confirmar_senha]

    for field in fields:
        if field is None:
            msg.add_message(
                request,
                constants.ERROR,
                "Não deixe nenhum campo em branco",
            )
            return False

    if User.objects.complex_filter(Q(username=usuario) | Q(email=email)).exists():
        msg.add_message(request, constants.ERROR, "Este usuário já existe")
        return False

    if len(senha) < 6:
        msg.add_message(request, constants.ERROR, "Sua senha tem menos de 8 digitos")
        return False

    if not re.search(r'["A-Z"]', senha):  # TODO: possivel erro
        print("erro em upper compile")
        msg.add_message(
            request, constants.ERROR, "Sua senha não possuí nenhuma letra maiusculo"
        )
        return False

    if not re.search(r'["a-z"]', senha):  # TODO: possivel erro
        msg.add_message(
            request, constants.ERROR, "Sua senha não possuí nenhuma letra minuscula"
        )
        return False

    if not re.search(r'["0-9"]', senha):  # TODO: possivel erro
        msg.add_message(request, constants.ERROR, "Sua senha não possuí nenhum número")
        return False

    if senha != confirmar_senha:
        msg.add_message(request, constants.ERROR, "As senhas são diferentes")
        return False

    return True
