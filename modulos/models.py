from django.db import models


class Modulo(models.Model):
	nombre = models.CharField(max_length = 20)
	horario_inicio = models.TimeField()
	horario_final = models.TimeField()
	ubicacion = models.TextField(blank=True)
	funciona = models.BooleanField()

	def __str__(self):
		return self.nombre
