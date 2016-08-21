"""MOIT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from modulos.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^inicio_min/$', inicio_min, name='inicio_min'),
    url(r'^$', inicio, name='inicio'),
    url(r'^login/$', login_persona, name='login_persona'),
    url(r'^logout/$', logout_persona, name='logout_persona'),
    url(r'^cambiar_modulo/(?P<nombre_modulo>.+)/$', cambiar_modulo, name='cambiar_modulo'),
    url(r'^editar_modulo/(?P<pk_modulo>[0-9]{1,2})/$', editar_modulo, name='editar_modulo'),
    url(r'^modulos_log/$', modulos_log, name='modulos_log'),
    url(r'^lista_modulos_cerrados/$', lista_modulos_cerrados, name='lista_modulos_cerrados'),
    url(r'^agregar_modulo_cerrado/$', agregar_modulo_cerrado, name='agregar_modulo_cerrado'),
    url(r'^editar_modulo_cerrado/(?P<pk_modulo_cerrado>[0-9]{1,2})/$', editar_modulo_cerrado, name='editar_modulo_cerrado'),
    url(r'^borrar_modulo_cerrado/(?P<pk_modulo_cerrado>[0-9]{1,2})/$', borrar_modulo_cerrado, name='borrar_modulo_cerrado'),
]

admin.site.site_header = 'Administracion de MOIT'
