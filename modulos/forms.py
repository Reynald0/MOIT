# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class LogPersona(forms.Form):
    usuario = forms.CharField(min_length=5,widget=forms.TextInput(attrs={'id': 'Usuario'}))
    clave = forms.CharField(min_length=5, widget=forms.PasswordInput(attrs={'id': 'Clave'}))

    def clean_usuario(self):
        #Comprueba que exista un username en la base de datos
        usuario = self.cleaned_data['usuario']
        if not User.objects.filter(username=usuario.title()):
            raise forms.ValidationError('El nombre de usuario no existe!')
        return usuario
