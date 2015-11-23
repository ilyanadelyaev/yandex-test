import django.conf.urls

import view.views


urlpatterns = [
    django.conf.urls.url(r'^$', view.views.SearchView.search, name='search'),
    django.conf.urls.url(r'^search$', view.views.SearchView.search_results, name='search_results'),
    django.conf.urls.url(r'^stations/$', view.views.StationIndexView.as_view(), name='stations_index'),
    django.conf.urls.url(r'^stations/(?P<pk>[0-9]+)/$', view.views.StationDetailView.as_view(), name='stations_detail'),
    django.conf.urls.url(r'^directions/$', view.views.DirectionIndexView.as_view(), name='directions_index'),
    django.conf.urls.url(r'^directions/(?P<pk>[0-9]+)/$', view.views.DirectionDetailView.as_view(), name='directions_detail'),
    django.conf.urls.url(r'^routes/$', view.views.RouteIndexView.as_view(), name='routes_index'),
    django.conf.urls.url(r'^routes/(?P<pk>[0-9]+)/$', view.views.RouteDetailView.as_view(), name='routes_detail'),
]
