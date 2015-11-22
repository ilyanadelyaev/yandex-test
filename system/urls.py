from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('lib.urls', namespace='lib')),

    url(r'^admin/', include(admin.site.urls)),
]
