import django.conf.urls

import api.views


urlpatterns = [
    django.conf.urls.url(r'^search$', api.views.SearchAPI.search, name='search'),
]
