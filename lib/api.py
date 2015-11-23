import json

import django.http


class SearchAPI(object):
    @staticmethod
    def search(request):
        data = json.dumps({'dummy': 1})
        return django.http.HttpResponse(data, content_type='application/json')


# urls

from django.conf.urls import url

urlpatterns = [
    url(r'^search$', SearchAPI.search, name='search'),
]
