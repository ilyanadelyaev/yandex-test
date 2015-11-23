from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('lib.views', namespace='view')),
    url(r'^api/', include('lib.api', namespace='api')),

    url(r'^admin/', include(admin.site.urls)),
]
