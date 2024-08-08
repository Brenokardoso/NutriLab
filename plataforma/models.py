from django.db import models
from django.contrib.auth.models import User


class Pacientes(models.Model):
    choices_sexo = (("F", "Femnino"), ("M", "Masculino"))
    nome = models.CharField(
        max_length=75,
        verbose_name="Nome",
        null=False,
        blank=False,
    )
    idade = models.PositiveIntegerField(
        verbose_name="Idade",
        null=False,
        blank=False,
    )
    sexo = models.CharField(
        max_length=1, verbose_name="Sexo", choices=choices_sexo, null=False, blank=False
    )
    email = models.EmailField(verbose_name="Email", null=False, blank=False)
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone",
        null=False,
        blank=False,
    )
    nutri = models.ForeignKey(
        User,
        models.CASCADE,
    )

    def __str__(self):
        return f"{self.nome} - {self.email}"
