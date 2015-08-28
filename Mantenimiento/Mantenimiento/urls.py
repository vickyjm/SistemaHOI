from django.conf.urls import patterns, include, url
from django.contrib import admin
from app_HOI import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.inicio_sesion,name = 'inicio_sesion'),
    url(r'^registrar',views.registro,name = 'registrar'),
    url(r'^recuperarContraseña$', views.recuperarContraseña, name = 'recuperarContraseña'),
    url(r'^crearItem',views.crearItem,name = 'crearItem'),
    url(r'^categorias$',views.categoria,name = 'categoria'),
    url(r'^categorias/(?P<_id>\d+)/editar',views.categoria_editar,name = 'categoria_editar'),
    url(r'^inventario',views.inventario,name = 'inventario'),
    url(r'^verperfil$', views.verperfil, name = 'verperfil')
)
