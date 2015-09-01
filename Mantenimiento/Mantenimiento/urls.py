from django.conf.urls import patterns, include, url
from django.contrib import admin
from app_HOI import views
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.inicio_sesion,name = 'inicio_sesion'),
    url(r'^registro',views.registro,name = 'registro'),
    url(r'^recuperarContraseña$', views.recuperarContraseña, name = 'recuperarContraseña'),
    url(r'^crearItem',views.crearItem,name = 'crearItem'),
    url(r'^categorias$',views.categoria,name = 'categoria'),
    url(r'^categorias/(?P<_id>\d+)/editar',views.categoria_editar,name = 'categoria_editar'),
    url(r'^inventario$',views.inventario,name = 'inventario'),
    url(r'^inventario/(?P<_id>\d+)/editar',views.item_editar,name = 'item_editar'),
    url(r'^verperfil$', views.verperfil, name = 'verperfil'),
    url(r'^cerrarSesion$', views.cerrarSesion, name = 'cerrarSesion')
)

urlpatterns += patterns('', (
    r'^static/(?P<path>.*)$',
    'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}
))
