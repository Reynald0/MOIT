from django.contrib import admin
from .models import Modulo, Modulo_Log

class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'horario_inicio', 'horario_final', 'ubicacion', 'funciona')

class ModuloLogAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_hora', 'modulo')

admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Modulo_Log, ModuloLogAdmin)
