import json

import django.db.models

import django.http

import core.models
import core.logic
import lib.tools


def _station_dict(o, extended=False):
    ret = {
        'id': o.id,
        'name': o.name,
    }
    if extended:
        ret['directions_count'] = o.directionstation_set.count()
        ret['routes_count'] = o.routestation_set.count()
    return ret

def _direction_dict(o, extended=False):
    ret = {
        'id': o.id,
        'name': o.name,
    }
    if extended:
        ret['stations_count'] = o.directionstation_set.count(),
        ret['routes_count'] = o.route_set.count(),
    return ret

def _directionstation_dict(o):
    return {
        'direction': {'id': o.direction.id, 'name': o.direction.name},
        'station': {'id': o.station.id, 'name': o.station.name},
        'position': o.position,
    }

def _route_dict(o, extended=False):
    ret = {
        'id': o.id,
        'name': o.name,
        'direction': {'id': o.direction.id, 'name': o.direction.name},
    }
    if extended:
        ret['travel_time'] = str(
            o.routestation_set.aggregate(django.db.models.Sum('move_time'))['move_time__sum'] + \
            o.routestation_set.aggregate(django.db.models.Sum('wait_time'))['wait_time__sum']
        ),
        ret['station_count'] = o.routestation_set.count(),
        ret['timetable_count'] = o.timetable_set.count(),
    return ret

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

    @classmethod
    def tools(cls, request):
        ret = []
        if request.GET.get('tool') == 'weekday':
            ret = list(lib.tools.Weekday.choices)
        return cls._response(json.dumps(ret))


class SearchAPI(API):
    @classmethod
    def search(cls, request):
        start_station = request.GET.get('start_station')
        end_station = request.GET.get('end_station')
        weekday = request.GET.get('weekday')

        error = None
        try:
            routes = core.logic.search_routes(start_station, end_station, weekday)
        except core.logic.SearchExcepton as ex:
            error = str(ex)

        ret = {}

        if error:
            ret['error'] = error
        else:
            ret['start_station'] = _station_dict(core.models.Station.objects.get(pk=start_station))
            ret['end_station'] = _station_dict(core.models.Station.objects.get(pk=end_station))
            ret['weekday'] = lib.tools.Weekday(int(weekday))

            rr = ret.setdefault('path', [])
            for start, end, direction, route in routes:
                rr.append({
                    'start_station': _station_dict(start),
                    'end_station': _station_dict(end),
                    'direction': _direction_dict(direction),
                    'routes': [{'route': _route_dict(r), 'time': str(t)} for r, t in route]
                })

        return cls._response(json.dumps(ret))


class ViewAPI(API):
    @classmethod
    def station(cls, request, pk):
        o = core.models.Station.objects.filter(pk=pk).first()
        ret = _station_dict(o, extended=True)
        ret['directionstation'] = [_directionstation_dict(ds) for ds in o.directionstation_set.all()]
        ret['routesstation'] = [_routestation_dict(rs) for rs in o.routestation_set.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def stations_list(cls, request):
        ret = [_station_dict(s, extended=True) for s in core.models.Station.objects.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def direction(cls, request, pk):
        o = core.models.Direction.objects.filter(pk=pk).first()
        ret = _direction_dict(o, extended=True)
        ret['directionstation'] = [_directionstation_dict(ds) for ds in o.directionstation_set.all()]
        ret['route'] = [_route_dict(r, extended=True) for r in o.route_set.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def directions_list(cls, request):
        ret = [_direction_dict(d, extended=True) for d in core.models.Direction.objects.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def route(cls, request, pk):
        o = core.models.Route.objects.filter(pk=pk).first()
        ret = _route_dict(o, extended=True)
        ret['routesstation'] = [_routestation_dict(rs) for rs in o.routestation_set.all()]
        ret['timetable'] = [_timetable_dict(t) for t in o.timetable_set.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def routes_list(cls, request):
        ret = [_route_dict(r, extended=True) for r in core.models.Route.objects.all()]
        return cls._response(json.dumps(ret))
