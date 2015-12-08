import django.conf.urls

import trains.www.views


urlpatterns = [
    django.conf.urls.url(
        r'^$',
        trains.www.views.search,
        name='search'),
    django.conf.urls.url(
        r'^station/$',
        trains.www.views.stations_list,
        name='stations_list'),
    django.conf.urls.url(
        r'^station/(?P<pk>[0-9]+)/$',
        trains.www.views.station,
        name='station'),
    django.conf.urls.url(
        r'^direction/$',
        trains.www.views.directions_list,
        name='directions_list'),
    django.conf.urls.url(
        r'^direction/(?P<pk>[0-9]+)/$',
        trains.www.views.direction,
        name='direction'),
    django.conf.urls.url(
        r'^route/$',
        trains.www.views.routes_list,
        name='routes_list'),
    django.conf.urls.url(
        r'^route/(?P<pk>[0-9]+)/$',
        trains.www.views.route,
        name='route'),
]
