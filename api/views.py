import json

import django.db.models

import django.http

import core.models
import core.logic


def _station_dict(o):
    return {
        'id': o.id,
        'name': o.name,
        'directions_count': o.directionstation_set.count(),
        'routes_count': o.routestation_set.count(),
    }

def _direction_dict(o):
    return {
        'id': o.id,
        'name': o.name,
        'stations_count': o.directionstation_set.count(),
        'routes_count': o.route_set.count(),
    }

def _directionstation_dict(o):
    return {
        'direction': {'id': o.direction.id, 'name': o.direction.name},
        'station': {'id': o.station.id, 'name': o.station.name},
        'position': o.position,
    }

def _route_dict(o):
    return {
        'id': o.id,
        'name': o.name,
        'direction': {'id': o.direction.id, 'name': o.direction.name},
        'travel_time': str(
            o.routestation_set.aggregate(django.db.models.Sum('move_time'))['move_time__sum'] + \
            o.routestation_set.aggregate(django.db.models.Sum('wait_time'))['wait_time__sum']
        ),
        'station_count': o.routestation_set.count(),
        'timetable_count': o.timetable_set.count(),
    }

def _routestation_dict(o):
    return {
        'route': {'id': o.route.id, 'name': o.route.name},
        'station': {'id': o.station.id, 'name': o.station.name},
        'position': o.position,
        'wait_time': str(o.wait_time) if o.wait_time else '-',
        'move_time': str(o.move_time) if o.move_time else '-',
    }

def _timetable_dict(o):
    return {
        'route': {'id': o.route.id, 'name': o.route.name},
        'weekday': o.weekday,
        'time': str(o.time),
    }


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
        o = core.models.Station.objects.filter(pk=pk).first()
        ret = _station_dict(o)
        ret['directionstation'] = [_directionstation_dict(ds) for ds in o.directionstation_set.all()]
        ret['routesstation'] = [_routestation_dict(rs) for rs in o.routestation_set.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def stations_list(cls, request):
        ret = [_station_dict(s) for s in core.models.Station.objects.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def direction(cls, request, pk):
        o = core.models.Direction.objects.filter(pk=pk).first()
        ret = _direction_dict(o)
        ret['directionstation'] = [_directionstation_dict(ds) for ds in o.directionstation_set.all()]
        ret['route'] = [_route_dict(rs) for rs in o.route_set.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def directions_list(cls, request):
        ret = [_direction_dict(d) for d in core.models.Direction.objects.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def route(cls, request, pk):
        o = core.models.Route.objects.filter(pk=pk).first()
        ret = _route_dict(o)
        ret['routesstation'] = [_routestation_dict(rs) for rs in o.routestation_set.all()]
        ret['timetable'] = [_timetable_dict(t) for t in o.timetable_set.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def routes_list(cls, request):
        ret = [_route_dict(r) for r in core.models.Route.objects.all()]
        return cls._response(json.dumps(ret))
