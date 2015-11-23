import json

import django.http
import django.core.serializers

import core.models
import core.logic


class API(object):
    @staticmethod
    def _response(data):
        return django.http.HttpResponse(data, content_type='application/json')


class SearchAPI(API):
    @classmethod
    def search(cls, request):
        data = json.dumps({'dummy': 1})
        return cls.__response(data)


class ViewAPI(API):
    @classmethod
    def station(cls, request, pk):
        data = django.core.serializers.serialize('json', core.models.Station.objects.filter(pk=pk))
        return cls._response(data)

    @classmethod
    def stations_list(cls, request):
        data = django.core.serializers.serialize('json', core.models.Station.objects.all())
        return cls._response(data)

    @classmethod
    def direction(cls, request, pk):
        data = django.core.serializers.serialize('json', core.models.Direction.objects.filter(pk=pk))
        return cls._response(data)

    @classmethod
    def directions_list(cls, request):
        data = django.core.serializers.serialize('json', core.models.Direction.objects.all())
        return cls._response(data)

    @classmethod
    def route(cls, request, pk):
        data = django.core.serializers.serialize('json', core.models.Route.objects.filter(pk=pk))
        return cls._response(data)

    @classmethod
    def routes_list(cls, request):
        data = django.core.serializers.serialize('json', core.models.Direction.objects.all())
        return cls._response(data)
