from django.contrib import admin
from .models import Ativacao


@admin.register(Ativacao)
class AtivacaoAdmin(admin.ModelAdmin):
    list_display = ("user", "ativo", "token")
    readonly_fields = ("token",)
