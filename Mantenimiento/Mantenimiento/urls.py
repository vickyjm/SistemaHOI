from django.conf.urls import patterns, include, url
from django.contrib import admin
from app_HOI import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Mantenimiento.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.basecol1, name = 'base-1col'),
    url(r'^col21$', views.basecol21, name = 'base-2col1'),
    url(r'^col22$', views.basecol22, name = 'base-2col1'),
    url(r'^col3$', views.basecol3, name = 'base-3col'),
)
