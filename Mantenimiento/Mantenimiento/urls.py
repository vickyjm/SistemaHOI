from django.conf.urls import patterns, include, url
from django.contrib import admin
from app_HOI import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Mantenimiento.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.basecol1, name = 'base-col1'),
    url(r'^col21$', views.basecol21, name = 'base-col21'),
    url(r'^col22$', views.basecol22, name = 'base-col21'),
    url(r'^col3$', views.basecol3, name = 'base-col3'),
    url(r'^verperfil$', views.verperfil, name = 'verperfil'),
)
