import uuid
import json
import datetime

import django.test

import trains.core.models


class SearchAPITests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()
        #
        stations = [
            'Prague',
            'Berlin',
            'Paris',
            'International Space Station',
        ]
        for station in stations:
            trains.core.models.Station(name=station).save()
        #
        directions = [
            'Prague - Berlin',
            'Berlin - Paris',
        ]
        for direction in directions:
            trains.core.models.Direction(name=direction).save()
        #
        directionstation = [
            ('Prague - Berlin', 'Prague', 0),
            ('Prague - Berlin', 'Berlin', 1),
            ('Berlin - Paris', 'Berlin', 0),
            ('Berlin - Paris', 'Paris', 1),
        ]
        for direction, station, position in directionstation:
            trains.core.models.Direction.objects.filter(name=direction).first().directionstation_set.create(
                    station=trains.core.models.Station.objects.filter(name=station).first(),
                    position=position,
            )
        #
        routes = [
            ('Prague - Berlin', 'Prague - Berlin', 'Prague', 'Berlin'),
            ('Berlin - Prague', 'Prague - Berlin', 'Berlin', 'Prague'),
            ('Berlin - Paris', 'Berlin - Paris', 'Berlin', 'Paris'),
            ('Paris - Berlin', 'Berlin - Paris', 'Paris', 'Berlin'),
        ]
        for route, direction, start_station, end_station, in routes:
            trains.core.models.Route(
                name=route,
                direction=trains.core.models.Direction.objects.filter(name=direction).first(),
                start_station=trains.core.models.Station.objects.filter(name=start_station).first(),
                end_station=trains.core.models.Station.objects.filter(name=end_station).first(),
            ).save()
        #
        routestation = [
            ('Prague - Berlin', 'Prague', '00:00', '04:00'),
            ('Prague - Berlin', 'Berlin', '00:00', '00:00'),
            ('Berlin - Prague', 'Berlin', '00:00', '04:00'),
            ('Berlin - Prague', 'Prague', '00:00', '00:00'),

            ('Berlin - Paris', 'Berlin', '00:00', '03:00'),
            ('Berlin - Paris', 'Paris', '00:00', '00:00'),
            ('Paris - Berlin', 'Paris', '00:00', '03:00'),
            ('Paris - Berlin', 'Berlin', '00:00', '00:00'),
        ]
        for route, station, wait_time, move_time in routestation:
            wait_time = datetime.datetime.strptime(wait_time, '%H:%M')
            wait_time = datetime.timedelta(hours=wait_time.hour, minutes=wait_time.minute)
            move_time = datetime.datetime.strptime(move_time, '%H:%M')
            move_time = datetime.timedelta(hours=move_time.hour, minutes=move_time.minute)
            trains.core.models.Route.objects.filter(name=route).first().routestation_set.create(
                station=trains.core.models.Station.objects.filter(name=station).first(),
                wait_time=wait_time,
                move_time=move_time,
            )
        #
        timetable = [
            ('Prague - Berlin', 0, '08:00'),
            ('Berlin - Prague', 0, '08:00'),
            ('Berlin - Paris', 0, '08:00'),
            ('Paris - Berlin', 0, '08:00'),
        ]
        for route, weekday, time in timetable:
            time = datetime.datetime.strptime(time, '%H:%M')
            trains.core.models.Route.objects.filter(name=route).first().timetable_set.create(
                weekday=weekday,
                time=time,
            )

    def test__search__one_direction(self):
        s1 = trains.core.models.Station.objects.get(name='Berlin')
        s2 = trains.core.models.Station.objects.get(name='Prague')
        d = trains.core.models.Direction.objects.get(name='Prague - Berlin')
        r = trains.core.models.Route.objects.get(name='Berlin - Prague')
        tt = trains.core.models.Timetable.objects.filter(route=r).first()
        #
        resp = self.client.get('/api/search/', {'start_station': s1.id, 'end_station': s2.id, 'date': '11/16/2015'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        #
        self.assertIn('path', content)
        self.assertEqual(content['path'][0]['start_station']['name'], s1.name)
        self.assertEqual(content['path'][0]['end_station']['name'], s2.name)
        self.assertEqual(content['path'][0]['direction']['name'], d.name)
        self.assertIn('routes', content['path'][0])
        self.assertEqual(content['path'][0]['routes'][0]['route']['name'], r.name)
        self.assertEqual(content['path'][0]['routes'][0]['time'], str(tt.time))

    def test__search__multiple_directions(self):
        s1 = trains.core.models.Station.objects.get(name='Paris')
        s2 = trains.core.models.Station.objects.get(name='Berlin')
        s3 = trains.core.models.Station.objects.get(name='Prague')
        d1 = trains.core.models.Direction.objects.get(name='Berlin - Paris')
        d2 = trains.core.models.Direction.objects.get(name='Prague - Berlin')
        r1 = trains.core.models.Route.objects.get(name='Paris - Berlin')
        r2 = trains.core.models.Route.objects.get(name='Berlin - Prague')
        tt1 = trains.core.models.Timetable.objects.filter(route=r1).first()
        tt2 = trains.core.models.Timetable.objects.filter(route=r2).first()
        #
        resp = self.client.get('/api/search/', {'start_station': s1.id, 'end_station': s3.id, 'date': '11/16/2015'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        #
        self.assertEqual(content['path'][0]['start_station']['name'], s1.name)
        self.assertEqual(content['path'][0]['end_station']['name'], s2.name)
        self.assertEqual(content['path'][0]['direction']['name'], d1.name)
        self.assertEqual(content['path'][0]['routes'][0]['route']['name'], r1.name)
        self.assertEqual(content['path'][0]['routes'][0]['time'], str(tt1.time))
        self.assertEqual(content['path'][1]['start_station']['name'], s2.name)
        self.assertEqual(content['path'][1]['end_station']['name'], s3.name)
        self.assertEqual(content['path'][1]['direction']['name'], d2.name)
        self.assertEqual(content['path'][1]['routes'][0]['route']['name'], r2.name)
        self.assertEqual(content['path'][1]['routes'][0]['time'], str(tt2.time))

    def test__search__empty_arguments_list(self):
        resp = self.client.get('/api/search/')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        #
        self.assertIn('error', content)

    def test__search__invalid_arguments_list(self):
        resp = self.client.get('/api/search/', {'start_station': 'a', 'end_station': 'b', 'date': '11/16/2015'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        #
        self.assertIn('error', content)

    def test__search__equal_station_ids(self):
        resp = self.client.get('/api/search/', {'start_station': 1, 'end_station': 1, 'date': '11/16/2015'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        #
        self.assertIn('error', content)

    def test__search__invalid__no_bounds_stations(self):
        s1 = trains.core.models.Station.objects.get(name='Paris')
        s2 = trains.core.models.Station.objects.get(name='International Space Station')
        #
        resp = self.client.get('/api/search/', {'start_station': s1.id, 'end_station': s2.id, 'date': '11/16/2015'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        #
        self.assertIn('error', content)


class ViewAPITests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test__stations_list(self):
        sn = str(uuid.uuid4())
        s = trains.core.models.Station(name=sn)
        s.save()
        #
        resp = self.client.get('/api/station/')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        obj = filter(lambda x: x['name'] == sn, content)[0]
        self.assertEqual(obj['id'], s.id)
        self.assertEqual(obj['name'], s.name)
        self.assertIn('directions_count', obj)
        self.assertIn('routes_count', obj)

    def test__station(self):
        sn = str(uuid.uuid4())
        s = trains.core.models.Station(name=sn)
        s.save()
        #
        resp = self.client.get('/api/station/{}/'.format(s.id))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['name'], s.name)
        self.assertEqual(content['id'], s.id)
        self.assertIn('directions_count', content)
        self.assertIn('routes_count', content)

    def test__directions_list(self):
        dn = str(uuid.uuid4())
        d = trains.core.models.Direction(name=dn)
        d.save()
        #
        resp = self.client.get('/api/direction/')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        obj = filter(lambda x: x['name'] == dn, content)[0]
        self.assertEqual(obj['id'], d.id)
        self.assertEqual(obj['name'], d.name)
        self.assertIn('stations_count', obj)
        self.assertIn('routes_count', obj)

    def test__direction(self):
        dn = str(uuid.uuid4())
        d = trains.core.models.Direction(name=dn)
        d.save()
        #
        resp = self.client.get('/api/direction/{}/'.format(d.id))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['name'], d.name)
        self.assertEqual(content['id'], d.id)
        self.assertIn('stations_count', content)
        self.assertIn('routes_count', content)

    def test__route_list(self):
        sn = str(uuid.uuid4())
        s = trains.core.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.core.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.core.models.Route(name=rn, direction=d, start_station=s, end_station=s)
        r.save()
        #
        resp = self.client.get('/api/route/')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        obj = filter(lambda x: x['name'] == rn, content)[0]
        self.assertEqual(obj['id'], d.id)
        self.assertEqual(obj['name'], r.name)
        self.assertEqual(obj['start_station']['id'], s.id)
        self.assertEqual(obj['end_station']['name'], sn)
        self.assertEqual(obj['travel_time'], '-')
        self.assertIn('station_count', obj)
        self.assertIn('timetable_count', obj)

    def test__route(self):
        sn = str(uuid.uuid4())
        s = trains.core.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.core.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.core.models.Route(name=rn, direction=d, start_station=s, end_station=s)
        r.save()
        #
        resp = self.client.get('/api/route/{}/'.format(r.id))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['name'], r.name)
        self.assertEqual(content['id'], r.id)
        self.assertEqual(content['start_station']['id'], s.id)
        self.assertEqual(content['end_station']['name'], sn)
        self.assertEqual(content['travel_time'], '-')
        self.assertIn('station_count', content)
        self.assertIn('timetable_count', content)

    def test__tools__weekdays(self):
        resp = self.client.get('/api/tools/', {'tool': 'weekdays'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn([0, 'Monday'], content)
        self.assertIn([6, 'Sunday'], content)

    def test__tools__timeintervals(self):
        resp = self.client.get('/api/tools/', {'tool': 'timeintervals'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn([0, None], content)
        self.assertIn([5, [21, 24]], content)
