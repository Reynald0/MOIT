import datetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Modulo
from .forms import LogPersona

modulos_cerrados = ['Oficinas CTT (3)', 'Palacio Municipal', 'Base 4 (2)', 'Plantel 2', 'Plantel 28', 'UJAT Central', 'UJAT DACS']
dias_cerrados = ['Saturday', 'Sunday']
dias_semana = ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sáb']


def ajustar_horario(Pmodulos, pDia_Sistema):
    for modulo in Pmodulos:
        if modulo.nombre == 'Planeta Papel' and pDia_Sistema == 'Saturday':
            modulo.horario_final = datetime.datetime.strptime('18:00:00', '%H:%M:%S').time()
        elif modulo.nombre == 'Planeta Papel' and pDia_Sistema == 'Sunday':
            modulo.horario_inicio = datetime.datetime.strptime('10:00:00', '%H:%M:%S').time()
            modulo.horario_final = datetime.datetime.strptime('18:00:00', '%H:%M:%S').time()
        elif modulo.nombre == 'Ex-DGTIC (2)' and pDia_Sistema == 'Saturday':
            modulo.horario_final = datetime.datetime.strptime('14:00:00', '%H:%M:%S').time()

def inicio(request):
    fecha_actual = datetime.datetime.now() - datetime.timedelta(hours=5)
    dia_sistema = fecha_actual.strftime("%A")
    dia_semana = dias_semana[int(fecha_actual.strftime("%w"))]
    hora_sistema = fecha_actual.hour
    minuto_sistema = fecha_actual.minute
    modulos = Modulo.objects.all()
    ajustar_horario(modulos, dia_sistema)
    return render(request, 'inicio.html', 
        {'fecha_actual': fecha_actual, 
        'dia' : dia_sistema ,
        'dia_semana': dia_semana,
        'hora_sistema': hora_sistema, 
        'minuto_sistema': minuto_sistema, 
        'modulos': modulos,
        'dias_cerrados' : dias_cerrados,
        'modulos_cerrados' : modulos_cerrados})

def cambiar_modulo(request, nombre_modulo):
	modulo = Modulo.objects.get(nombre=nombre_modulo) 
	modulo.funciona = not modulo.funciona
	modulo.save()
	return redirect('inicio')

def inicio_min(request):
    fecha_actual = datetime.datetime.now() - datetime.timedelta(hours=5)
    dia_sistema = fecha_actual.strftime("%A")
    dia_semana = dias_semana[int(fecha_actual.strftime("%w"))]
    hora_sistema = fecha_actual.hour
    minuto_sistema = fecha_actual.minute
    modulos = Modulo.objects.all()
    ajustar_horario(modulos, dia_sistema)
    return render(request, 'inicio_min.html', 
        {'fecha_actual': fecha_actual, 
        'dia' : dia_sistema ,
        'dia_semana': dia_semana,
        'hora_sistema': hora_sistema, 
        'minuto_sistema': minuto_sistema, 
        'modulos': modulos,
        'dias_cerrados' : dias_cerrados,
        'modulos_cerrados' : modulos_cerrados})

def login_persona(request):
    error = False
    if request.method == 'POST': #Si el formulario envia algo con el metodo POST
        form = LogPersona(request.POST) #Se crea el objeto form, a este objeto se le asigna el modelo LogPersona
        if form.is_valid(): #Si el formulario es valido
            usuario = request.POST.get('usuario') #Se obtiene el valor del campo usuario
            clave = request.POST.get('clave') #Se obtiene el valor del campo clave
            # Se crea un objeto individuo el cual es la autenticacion con las variables usuario y clave
            usuario_persona = authenticate(username=usuario.title(), password=clave)
            # Si existe algun  usuario_persona, es decir, ha sido registrado el usuario que se trata de logear
            if usuario_persona is not None:
                # Si el individuo esta activo en el sistema (osea no esta dado de baja)
                # No estoy seguro de esto!
                if usuario_persona.is_active:
                    login(request, usuario_persona) # Se usa el metodo log() que recibe como argumento a request y al objeto individuo
                    # Se redirige al la vista llamada inicio.
                    # Para saber como se llama cada vista hay que ver el valor de la variable 'name' en el urls.py
                    # En este caso la url llamada inicio es el inicio del sitio web
                    return redirect('inicio')
            else: # De lo contrario, el usuario no ha sido registrado
                error = True
                # Regresa el html 'login' renderizado y con el formulario rellenado a como lo dejo la persona
                # tambien la variable error (Booleano)
                return render(request, 'login.html', {'form' : form, 'error': error})
        else: # De lo contrario, el formulario no es valido
            # Regresa el html 'login' renderizado con la variable form, que es el formulario previamente rellenado
            return render(request, 'login.html', {'form' : form})
    else: #De lo contrario, la persona esta apenas por registrarse
        #Se crea el bojeto form con el formulario LogPersona
        form = LogPersona()
        #Regresa el html 'login' renderizado con la variable form en blanco.
        return render(request, 'login.html', {'form' : form})

def logout_persona(request): #Se define la funcion logout_persona el cual es el nombre de la vista a mostrar
    logout(request) #Se usa el metodo logout() que recibe el request
    # Regresa la vista inicio y como inicio necesita request, entonces se le pasa el request de log_persona
    return redirect('inicio')