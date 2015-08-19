from django.conf.urls import patterns, include, url
from django.contrib import admin
from app_HOI.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Mantenimiento.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',inicio_sesion,name = "inicio_sesion"),
)
