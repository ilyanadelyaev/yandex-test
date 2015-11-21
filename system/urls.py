from django.conf.urls import include, url
from django.contrib import admin

import lib.views


urlpatterns = [
    url(r'^$', lib.views.index, name='index'),

    url(r'^', include('lib.urls', namespace='lib')),

    url(r'^admin/', include(admin.site.urls)),
]
