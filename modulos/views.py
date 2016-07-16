from django.shortcuts import render
from django.utils import timezone
import datetime
from .models import Modulo

def inicio(request):
	fecha_actual = datetime.datetime.now() - datetime.timedelta(hours=5)
	modulos = Modulo.objects.all()
	return render(request, 'inicio.html', {'fecha_actual': fecha_actual, 'modulos': modulos })

