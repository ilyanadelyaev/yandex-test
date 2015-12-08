import json

import django.db.models

import django.http

import trains.models
import trains.tools
import trains.logic.search
import trains.logic.errors


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
        'start_station': {'id': o.start_station.id, 'name': o.start_station.name},
        'end_station': {'id': o.end_station.id, 'name': o.end_station.name},
    }
    if extended:
        traveltime = '-'
        if o.routestation_set.count():
            traveltime = str(
                o.routestation_set.aggregate(django.db.models.Sum('move_time'))['move_time__sum'] + \
                o.routestation_set.aggregate(django.db.models.Sum('wait_time'))['wait_time__sum']
            )
        ret['travel_time'] = traveltime
        ret['station_count'] = o.routestation_set.count(),
        ret['timetable_count'] = o.timetable_set.count(),
    return ret

def _routestation_dict(o):
    return {
        'route': {'id': o.route.id, 'name': o.route.name},
        'station': {'id': o.station.id, 'name': o.station.name},
        'wait_time': str(o.wait_time) if o.wait_time else '-',
        'move_time': str(o.move_time) if o.move_time else '-',
    }

def _timetable_dict(o):
    return {
        'route': {'id': o.route.id, 'name': o.route.name},
        'weekday': trains.tools.Weekday(o.weekday),
        'time': str(o.time),
    }


class API(object):
    @staticmethod
    def _response(data):
        return django.http.HttpResponse(data, content_type='application/json')


class SearchAPI(API):
    @classmethod
    def search(cls, request):
        start_station = request.GET.get('start_station')
        end_station = request.GET.get('end_station')
        date = request.GET.get('date')

        timeinterval = request.GET.get('timeinterval')
        timeinterval = trains.tools.TimeInterval(timeinterval)

        error = None
        try:
            routes = trains.logic.search.search_routes(
                start_station, end_station, date, timeinterval)
        except trains.logic.errors.SearchExcepton as ex:
            error = str(ex)

        ret = {}

        if error:
            ret['error'] = error
        else:
            ret['start_station'] = _station_dict(trains.models.Station.objects.get(pk=start_station))
            ret['end_station'] = _station_dict(trains.models.Station.objects.get(pk=end_station))
            ret['date'] = date

            rr = ret.setdefault('path', [])
            for obj in routes:
                rr.append({
                    'start_station': _station_dict(obj['start_station']),
                    'end_station': _station_dict(obj['end_station']),
                    'direction': _direction_dict(obj['direction']),
                    'routes': [{'route': _route_dict(o['route']), 'time': str(o['time'])} for o in obj['routes']]
                })

        return cls._response(json.dumps(ret))


class ViewAPI(API):
    @classmethod
    def station(cls, request, pk):
        o = trains.models.Station.objects.filter(pk=pk).first()
        ret = _station_dict(o, extended=True)
        ret['directionstation'] = [_directionstation_dict(ds) for ds in o.directionstation_set.all()]
        ret['routesstation'] = [_routestation_dict(rs) for rs in o.routestation_set.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def stations_list(cls, request):
        ret = [_station_dict(s, extended=True) for s in trains.models.Station.objects.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def direction(cls, request, pk):
        o = trains.models.Direction.objects.filter(pk=pk).first()
        ret = _direction_dict(o, extended=True)
        ret['directionstation'] = [_directionstation_dict(ds) for ds in o.directionstation_set.all()]
        ret['route'] = [_route_dict(r, extended=True) for r in o.route_set.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def directions_list(cls, request):
        ret = [_direction_dict(d, extended=True) for d in trains.models.Direction.objects.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def route(cls, request, pk):
        o = trains.models.Route.objects.filter(pk=pk).first()
        ret = _route_dict(o, extended=True)
        ret['routesstation'] = [_routestation_dict(rs) for rs in o.routestation_set.all()]
        ret['timetable'] = [_timetable_dict(t) for t in o.timetable_set.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def routes_list(cls, request):
        ret = [_route_dict(r, extended=True) for r in trains.models.Route.objects.all()]
        return cls._response(json.dumps(ret))

    @classmethod
    def tools(cls, request):
        tool = request.GET.get('tool', '')
        ret = ''
        if tool == 'weekdays':
            ret = list(trains.tools.Weekday.choices)
        elif tool == 'timeintervals':
            ret = list(trains.tools.TimeInterval.choices)
        return cls._response(json.dumps(ret))
