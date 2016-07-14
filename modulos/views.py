from django.shortcuts import render
from django.utils import timezone
from .models import Modulo

def inicio(request):
	fecha_actual = timezone.now()
	modulos = Modulo.objects.all()
	return render(request, 'inicio.html', {'fecha_actual': fecha_actual, 'modulos': modulos })

