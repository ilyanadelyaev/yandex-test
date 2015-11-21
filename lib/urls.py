from django.conf.urls import include, url

import lib.views


urlpatterns = [
    url(r'^search/$', lib.views.search, name='search'),
    url(r'^search/results/$', lib.views.results, name='search_results'),

    url(r'^stations/$', lib.views.StationIndexView.as_view(), name='stations_index'),
    url(r'^stations/(?P<pk>[0-9]+)/$', lib.views.StationDetailView.as_view(), name='stations_detail'),
    url(r'^directions/$', lib.views.DirectionIndexView.as_view(), name='directions_index'),
    url(r'^directions/(?P<pk>[0-9]+)/$', lib.views.DirectionDetailView.as_view(), name='directions_detail'),
    url(r'^routes/$', lib.views.RouteIndexView.as_view(), name='routes_index'),
    url(r'^routes/(?P<pk>[0-9]+)/$', lib.views.RouteDetailView.as_view(), name='routes_detail'),
]
