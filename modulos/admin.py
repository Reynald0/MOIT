from django.contrib import admin
from .models import Modulo

class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'horario_inicio', 'horario_final', 'ubicacion', 'funciona')

admin.site.register(Modulo, ModuloAdmin)
