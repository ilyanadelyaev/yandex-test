import uuid
import json

import django.test

import trains.core.models


class SearchAPITests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test__search__one_direction(self):
        pass

    def test__search__multiple_directions(self):
        pass

    def test__search__invalid__arguments_list(self):
        pass

    def test__search__invalid__equal_station_ids(self):
        pass

    def test__search__invalid__no_bounds_stations(self):
        pass


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
        dn = str(uuid.uuid4())
        d = trains.core.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.core.models.Route(name=rn, direction=d)
        r.save()
        #
        resp = self.client.get('/api/route/')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        obj = filter(lambda x: x['name'] == rn, content)[0]
        self.assertEqual(obj['id'], d.id)
        self.assertEqual(obj['name'], r.name)
        self.assertEqual(obj['travel_time'], '-')
        self.assertIn('station_count', obj)
        self.assertIn('timetable_count', obj)

    def test__route(self):
        dn = str(uuid.uuid4())
        d = trains.core.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.core.models.Route(name=rn, direction=d)
        r.save()
        #
        resp = self.client.get('/api/route/{}/'.format(r.id))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['name'], r.name)
        self.assertEqual(content['id'], r.id)
        self.assertEqual(content['travel_time'], '-')
        self.assertIn('station_count', content)
        self.assertIn('timetable_count', content)

    def test__weekday(self):
        resp = self.client.get('/api/weekday/')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn([0, 'Monday'], content)
        self.assertIn([6, 'Sunday'], content)
