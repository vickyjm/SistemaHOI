from django.conf.urls import patterns, include, url
from django.contrib import admin
from app_HOI import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.inicio_sesion,name = 'inicio_sesion'),
    url(r'^registrar',views.registro,name = 'registrar'),
    url(r'^crearItem',views.crearItem,name = 'crearItem'),
    url(r'^categoria',views.categoria,name = 'categoria'),
    url(r'^inventario',views.inventario,name = 'inventario'),
    url(r'^col21$', views.basecol21, name = 'base-col21'),
    url(r'^col22$', views.basecol22, name = 'base-col21'),
    url(r'^col3$', views.basecol3, name = 'base-col3'),
    url(r'^verperfil$', views.verperfil, name = 'verperfil'),
)
