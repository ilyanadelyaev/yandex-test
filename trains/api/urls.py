import django.conf.urls

import trains.api.views


urlpatterns = [
    django.conf.urls.url(r'^search/$', trains.api.views.SearchAPI.search, name='search'),

    django.conf.urls.url(r'^station/(?P<pk>[0-9]+)/$', trains.api.views.ViewAPI.station, name='station'),
    django.conf.urls.url(r'^station/$', trains.api.views.ViewAPI.stations_list, name='stations_list'),
    django.conf.urls.url(r'^direction/(?P<pk>[0-9]+)/$', trains.api.views.ViewAPI.direction, name='direction'),
    django.conf.urls.url(r'^direction/$', trains.api.views.ViewAPI.directions_list, name='directions_list'),
    django.conf.urls.url(r'^route/(?P<pk>[0-9]+)/$', trains.api.views.ViewAPI.route, name='route'),
    django.conf.urls.url(r'^route/$', trains.api.views.ViewAPI.routes_list, name='routes_list'),
    django.conf.urls.url(r'^weekday/$', trains.api.views.ViewAPI.weekdays_list, name='weekdays_list'),
]
