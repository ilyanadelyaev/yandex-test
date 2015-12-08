import uuid

import django.test

import trains.models


class ViewTests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()
        #
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        self.station_id = s.id
        #
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        self.direction_id = d.id
        #
        rn = str(uuid.uuid4())
        r = trains.models.Route(name=rn, direction=d, start_station=s, end_station=s)
        r.save()
        self.route_id = r.id

    def test__invalid_url(self):
        resp = self.client.get('/index/')
        self.assertEqual(resp.status_code, 404)

    def test__search(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test__stations_list(self):
        resp = self.client.get('/station/')
        self.assertEqual(resp.status_code, 200)

    def test__station(self):
        resp = self.client.get('/station/{}/'.format(self.station_id))
        self.assertEqual(resp.status_code, 200)

    def test__directions_list(self):
        resp = self.client.get('/direction/')
        self.assertEqual(resp.status_code, 200)

    def test__direction(self):
        resp = self.client.get('/direction/{}/'.format(self.direction_id))
        self.assertEqual(resp.status_code, 200)

    def test__routes_list(self):
        resp = self.client.get('/route/')
        self.assertEqual(resp.status_code, 200)

    def test__route(self):
        resp = self.client.get('/route/{}/'.format(self.route_id))
        self.assertEqual(resp.status_code, 200)
