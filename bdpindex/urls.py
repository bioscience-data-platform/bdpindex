from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from bdpindex.searchengine import views

urlpatterns = patterns('bdpindex.searchengine',
    (r'^index/$', views.index),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()

