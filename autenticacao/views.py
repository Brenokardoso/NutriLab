from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q


def cadastro(request):

    usuario = request.POST.get("usuario")
    email = request.POST.get("email")
    senha = request.POST.get("senha")
    confirmar_senha = request.POST.get("confirmar_senha")

    print(f"valor de usuario {usuario}")
    print(f"valor de email {email}")
    print(f"valor de senha {senha}")
    print(f"valor de confirmar_senha {confirmar_senha}")

    if (
        len(
            User.objects.complex_filter(
                Q(username=usuario) & Q(email=email) & Q(password=senha)
            )
        )
        == 0
    ):
        if senha == confirmar_senha:
            try:
                user = User.objects.create_user(
                    username=usuario, email=email, password=senha
                )
                user.save()
                return render(request, "cadastro.html?status=200")

            except Exception as e:
                print(f"Houve uma excessão ao salvar os dados por motivos de {e}")
        else:
            print("Houve uma excessão ao confirmar a senha")

    else:
        print("Este usuário já existe")

    return render(request, "cadastro.html")


def login(request):
    return render(request, "login.html")
