import django.conf.urls

import api.views


urlpatterns = [
    django.conf.urls.url(r'^search$', api.views.SearchAPI.search, name='search'),

    django.conf.urls.url(r'^station/(?P<pk>[0-9]+)/$', api.views.ViewAPI.station, name='station'),
    django.conf.urls.url(r'^station$', api.views.ViewAPI.stations_list, name='stations_list'),
    django.conf.urls.url(r'^direction/(?P<pk>[0-9]+)/$', api.views.ViewAPI.direction, name='direction'),
    django.conf.urls.url(r'^direction$', api.views.ViewAPI.directions_list, name='directions_list'),
    django.conf.urls.url(r'^route/(?P<pk>[0-9]+)/$', api.views.ViewAPI.route, name='route'),
    django.conf.urls.url(r'^route$', api.views.ViewAPI.routes_list, name='routes_list'),
]
