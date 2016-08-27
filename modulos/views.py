import datetime
from django.contrib.admin.models import LogEntry
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Modulo, Modulo_Log, Modulo_Cerrado
from .forms import LogPersona, ModuloForm, ModuloCerradoForm

dias_semana = ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sáb']


def consultar_fecha():
    # Fecha y hora en UTC -5, por eso se le restan cinco horas, es la Time Zone de México
    fecha_actual = datetime.datetime.now() - datetime.timedelta(hours=5)
    return fecha_actual

def ajustar_dia(pDia_Sistema):
    modulos = Modulo_Cerrado.objects.filter(dia=pDia_Sistema)
    modulos_cerrados = []
    for modulo in modulos:
        modulos_cerrados.append(modulo.modulo.nombre)
    return modulos_cerrados

def registrar_cambio(pUsuario, pModulo):
    movimiento = Modulo_Log()
    movimiento.usuario = pUsuario
    #movimiento.fecha_hora = timezone.now() #Esta linea no es necesaria ya que en el models.py se define el Objeto Modulo_Log como auto_now=True
    movimiento.modulo = pModulo
    movimiento.save()

def ajustar_horario(Pmodulos, pDia_Sistema):
    for modulo in Pmodulos:
        if modulo.nombre == 'Planeta Papel' and pDia_Sistema == 'Saturday':
            modulo.horario_final = datetime.datetime.strptime('18:00:00', '%H:%M:%S').time()
        elif modulo.nombre == 'Planeta Papel' and pDia_Sistema == 'Sunday':
            modulo.horario_inicio = datetime.datetime.strptime('10:00:00', '%H:%M:%S').time()
            modulo.horario_final = datetime.datetime.strptime('18:00:00', '%H:%M:%S').time()
        elif modulo.nombre == 'Ex-DGTIC (2)' and pDia_Sistema == 'Saturday':
            modulo.horario_final = datetime.datetime.strptime('14:00:00', '%H:%M:%S').time()
        elif modulo.nombre == 'Base 4' and pDia_Sistema == 'Saturday':
            modulo.horario_inicio = datetime.datetime.strptime('09:00:00', '%H:%M:%S').time()
            modulo.horario_final = datetime.datetime.strptime('13:00:00', '%H:%M:%S').time()


def inicio(request):
    fecha_actual = consultar_fecha()
    dia_sistema = fecha_actual.strftime("%A")
    dia_semana = dias_semana[int(fecha_actual.strftime("%w"))]
    hora_sistema = fecha_actual.hour
    minuto_sistema = fecha_actual.minute
    modulos = Modulo.objects.all()
    modulos_cerrados = ajustar_dia(dia_sistema)
    ajustar_horario(modulos, dia_sistema)
    return render(request, 'no_modulos.html', 
        {'fecha_actual': fecha_actual, 
        'dia' : dia_sistema ,
        'dia_semana': dia_semana,
        'hora_sistema': hora_sistema, 
        'minuto_sistema': minuto_sistema, 
        'modulos': modulos,
        'modulos_cerrados' : modulos_cerrados})

@login_required
def cambiar_modulo(request, nombre_modulo):
    modulo = Modulo.objects.get(nombre=nombre_modulo) 
    modulo.funciona = not modulo.funciona
    modulo.save()
    registrar_cambio(request.user, modulo)
    return redirect('inicio')

@login_required
def editar_modulo(request, pk_modulo):
    usuario = request.user
    modulo = get_object_or_404(Modulo, pk=pk_modulo)
    if request.method == 'POST':
        form = ModuloForm(request.POST, instance=modulo)
        if form.is_valid():
            modulo = form.save(commit=False)
            modulo.save()
            registrar_cambio(request.user, modulo)
            return redirect('modulos.views.inicio')
    else:
        form = ModuloForm(instance=modulo)
        return render(request, 'editar_modulo.html', {'form': form})

def inicio_min(request):
    fecha_actual = consultar_fecha()
    dia_sistema = fecha_actual.strftime("%A")
    dia_semana = dias_semana[int(fecha_actual.strftime("%w"))]
    hora_sistema = fecha_actual.hour
    minuto_sistema = fecha_actual.minute
    modulos = Modulo.objects.all()
    modulos_cerrados = ajustar_dia(dia_sistema)
    ajustar_horario(modulos, dia_sistema)
    return render(request, 'no_modulos.html', 
        {'fecha_actual': fecha_actual, 
        'dia' : dia_sistema ,
        'dia_semana': dia_semana,
        'hora_sistema': hora_sistema, 
        'minuto_sistema': minuto_sistema, 
        'modulos': modulos,
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

@login_required
def modulos_log(request):
    movimientos = Modulo_Log.objects.filter(fecha_hora__lte=timezone.now()).order_by('-fecha_hora')[0:9] #Primeros 10 registros
    return render(request, 'modulos_log.html', {'movimientos': movimientos})

@login_required
def lista_modulos_cerrados(request):
    dias_modulos = []
    dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_semana_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    for dia in dias_semana:
        modulos_cerrados = Modulo_Cerrado.objects.filter(dia=dia)
        if modulos_cerrados:
            dias_modulos.append(modulos_cerrados)
    # Indice 0 es el Lunes, 1 es el Martes.....
    return render(request, 'lista_modulos_cerrados.html', 
        {'dias_modulos': dias_modulos, 
        'dias_semana_es' : dias_semana_es})

@login_required
def agregar_modulo_cerrado(request):
    if request.method == 'POST':
        form = ModuloCerradoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_modulos_cerrados')
        else:
            return render(request, 'agregar_modulo_cerrado.html', {'form' : form })
    else:
        form = ModuloCerradoForm()
        return render(request, 'agregar_modulo_cerrado.html', {'form' : form })

@login_required
def editar_modulo_cerrado(request, pk_modulo_cerrado):
    modulo = get_object_or_404(Modulo_Cerrado, pk=pk_modulo_cerrado)
    form = ModuloCerradoForm(instance=modulo)
    return render(request, 'editar_modulo_cerrado.html', {'form': form})

@login_required
def borrar_modulo_cerrado(request, pk_modulo_cerrado):
    modulo_cerrado = get_object_or_404(Modulo_Cerrado, pk=pk_modulo_cerrado)
    modulo_cerrado.delete()
    return redirect('lista_modulos_cerrados')