from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('www.urls', namespace='www')),
    url(r'^api/', include('api.urls', namespace='api')),

    url(r'^view/', include('view.urls', namespace='view')),  # debug

    url(r'^admin/', include(admin.site.urls)),
]
