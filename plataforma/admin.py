from django.contrib import admin
from .models import Pacientes


@admin.register(Pacientes)
class PacientesAdmin(admin.ModelAdmin):
    list_display = ["nome", "idade", "email", "sexo", "telefone", "nutri"]
    list_filter = ["nome"]
    search_fields = ["nome", "nutri"]
