from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()

from bdpindex.searchengine import views

urlpatterns = patterns('bdpindex.searchengine',
    (r'^hello/$', views.hello),
    (r'^index/$', views.index),
    url(r'^admin/', include(admin.site.urls)),
)
