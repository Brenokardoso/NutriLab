from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages as msg
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import re
import os


def validando_campos_cadastro(request, usuario, email, senha, confirmar_senha):

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

    elif len(senha) < 6:
        msg.add_message(request, constants.ERROR, "Sua senha tem menos de 8 digitos")
        return False

    elif not re.search(r'["A-Z"]', senha):
        print("erro em upper compile")
        msg.add_message(
            request, constants.ERROR, "Sua senha não possuí nenhuma letra maiusculo"
        )
        return False

    elif not re.search(r'["a-z"]', senha):
        msg.add_message(
            request, constants.ERROR, "Sua senha não possuí nenhuma letra minuscula"
        )
        return False

    elif not re.search(r'["0-9"]', senha):
        msg.add_message(request, constants.ERROR, "Sua senha não possuí nenhum número")
        return False

    elif senha != confirmar_senha:
        msg.add_message(request, constants.ERROR, "As senhas são diferentes")
        return False

    return True


def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:

    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, para
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {"status": 1}
