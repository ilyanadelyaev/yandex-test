from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('view.urls', namespace='view')),
    url(r'^api/', include('api.urls', namespace='api')),

    url(r'^admin/', include(admin.site.urls)),
]
