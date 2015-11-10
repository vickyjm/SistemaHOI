from django.conf.urls import patterns, include, url
from django.contrib import admin
from app_HOI import views
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import handler404, handler403

handler403 = 'app_HOI.views.permission_denied'
handler404 = 'app_HOI.views.page_not_found'

urlpatterns = patterns('',
    url(r'^$',views.inicio_sesion,name = 'inicio_sesion'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^categorias$',views.categoria,name = 'categorias'),
    url(r'^categorias/(?P<_id>\d+)/editar$',views.categoria_editar,name = 'categoria_editar'),
    url(r'^categorias/(?P<_id>\d+)/editar/estado$',views.categoria_estado, name = 'categoria_estado'),
    url(r'^cerrarSesion$', views.cerrarSesion, name = 'cerrarSesion'),
    url(r'^crearItem$',views.crearItem,name = 'crearItem'),
    url(r'^crearSolicitud',views.crearSolicitud,name = 'crearSolicitud'),
    url(r'^crearUsuario$',views.registro,name='crearUsuario'),
    url(r'^departamentos$',views.adminDptos,name='adminDptos'),
    url(r'^departamentos/(?P<_id>\d+)/editar',views.editarDpto,name='editarDpto'),
    url(r'^inventario$',views.inventario,name = 'inventario'),
    url(r'^inventario/(?P<_id>\d+)/editar$',views.item_editar,name = 'item_editar'),
    url(r'^inventario/(?P<_id>\d+)/editar/estado',views.item_estado,name = 'item_estado'),
    url(r'^inventario/(?P<_id>\d+)/ingresar', views.item_ingresar, name = 'item_ingresar'),
    url(r'^perfil/(?P<_id>\d+)/editar', views.perfil_editar, name = 'perfil_editar'),
    url(r'^cambiarContraseña$', views.cambiarContraseña, name = 'cambiarContraseña'),
    url(r'^recuperarContraseña$', views.recuperarContraseña, name = 'recuperarContraseña'),
    url(r'^registrar',views.registro,name = 'registrar'),
    url(r'^reporte$',views.imprimirReporte, name='reporte'),
    url(r'^solicitud$', views.solicitud, name = 'solicitud'),
    url(r'^solicitud/(?P<_id>\d+)/editar', views.solicitud_editar,name = 'solicitud_editar'),
    url(r'^solicitud/(?P<_id>\d+)/eliminar', views.solicitud_eliminar,name = 'solicitud_eliminar'),
    url(r'^solicitud_estado/(?P<_id>\d+)/(?P<_nuevo_estado>[A|R]+)', views.solicitud_estado,name = 'solicitud_estado'),
    url(r'^usuarios$',views.adminUsuarios,name='adminUsuarios'),
    url(r'^usuarios/(?P<_id>\d+)/editar$', views.editarUsuario,name = 'editarUsuario'),
    url(r'^verperfil$', views.verperfil, name = 'verperfil'),

)

urlpatterns += patterns('', (
    r'^static/(?P<path>.*)$',
    'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}
))
