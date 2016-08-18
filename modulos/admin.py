from django.contrib import admin
from .models import Modulo, Modulo_Log, Modulo_Cerrado

class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'horario_inicio', 'horario_final', 'ubicacion', 'funciona')

class ModuloLogAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_hora', 'modulo')

class ModuloCerradoAdmin(admin.ModelAdmin):
    list_display = ('dia', 'modulo',)

admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Modulo_Log, ModuloLogAdmin)
admin.site.register(Modulo_Cerrado, ModuloCerradoAdmin)
