import django.conf.urls

import www.views


urlpatterns = [
    django.conf.urls.url(r'^$', www.views.search, name='search'),
    django.conf.urls.url(r'^station/$', www.views.stations_list, name='stations_list'),
    django.conf.urls.url(r'^station/(?P<pk>[0-9]+)/$', www.views.station, name='station'),
    django.conf.urls.url(r'^direction/$', www.views.directions_list, name='directions_list'),
    django.conf.urls.url(r'^direction/(?P<pk>[0-9]+)/$', www.views.direction, name='direction'),
    django.conf.urls.url(r'^route/$', www.views.routes_list, name='routes_list'),
    django.conf.urls.url(r'^route/(?P<pk>[0-9]+)/$', www.views.route, name='route'),
]
