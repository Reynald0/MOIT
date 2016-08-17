from django.contrib.auth.models import User
from django.db import models


class Modulo(models.Model):
	nombre = models.CharField(max_length = 20)
	horario_inicio = models.TimeField()
	horario_final = models.TimeField()
	ubicacion = models.TextField(blank=True)
	funciona = models.BooleanField()

	def __str__(self):
		return self.nombre

class Modulo_Log(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha_hora = models.DateTimeField(auto_now=True)
	modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

	def __str__(self):
		return (self.usuario.username + ' modifica ' + self.modulo.nombre + ' el ' + self.fecha_hora.strftime('%c'))