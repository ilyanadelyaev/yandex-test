import uuid
import datetime

import django.test

import trains.models


class StationModelTests(django.test.TestCase):
    def test__has_fields(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        s = trains.models.Station.objects.get(pk=s.id)
        self.assertEqual(s.name, sn)

    def test__directionstation_list(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        self.assertEqual(len(s.directionstation_list()), 0)
        s.directionstation_set.create(direction=d, position=1)
        self.assertEqual(len(s.directionstation_list()), 1)
        ll = set(((i.direction.id, i.direction.name, i.position) for i in s.directionstation_list()))
        self.assertIn((d.id, dn, 1), ll)


class DirectionModelTests(django.test.TestCase):
    def test__has_fields(self):
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        d = trains.models.Direction.objects.get(pk=d.id)
        self.assertEqual(d.name, dn)


class DirectionStationModelTests(django.test.TestCase):
    def test__direct_creation(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        ds = trains.models.DirectionStation(
            direction=d, station=s, position=4)
        ds.save()
        ds = trains.models.DirectionStation.objects.filter(pk=ds.id).first()
        self.assertEqual(ds.direction.name, dn)
        self.assertEqual(ds.station.name, sn)
        self.assertEqual(ds.position, 4)

    def test__via_direction(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        ds = d.directionstation_set.create(station=s, position=5)
        ds = trains.models.DirectionStation.objects.filter(
            pk=ds.id).first()
        self.assertEqual(ds.direction.name, dn)
        self.assertEqual(ds.station.name, sn)
        self.assertEqual(ds.position, 5)

    def test__via_station(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        ds = s.directionstation_set.create(direction=d, position=6)
        ds = trains.models.DirectionStation.objects.filter(
            pk=ds.id).first()
        self.assertEqual(ds.direction.name, dn)
        self.assertEqual(ds.station.name, sn)
        self.assertEqual(ds.position, 6)


class RouteModelTests(django.test.TestCase):
    def test__has_fields(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.models.Route(name=rn, direction=d, start_station=s, end_station=s)
        r.save()
        r = trains.models.Route.objects.get(pk=r.id)
        self.assertEqual(r.name, rn)
        self.assertEqual(r.direction.name, dn)
        self.assertEqual(r.start_station.name, sn)
        self.assertEqual(r.end_station.name, sn)


class RouteStationModelTests(django.test.TestCase):
    def test__direct_creation(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.models.Route(name=rn, direction=d, start_station=s, end_station=s)
        r.save()
        rs = trains.models.RouteStation(
            route=r, station=s,
            wait_time=datetime.timedelta(1),
            move_time=datetime.timedelta(2),
        )
        rs.save()
        rs = trains.models.RouteStation.objects.filter(pk=rs.id).first()
        self.assertEqual(rs.route.name, rn)
        self.assertEqual(rs.station.name, sn)
        self.assertEqual(rs.wait_time, datetime.timedelta(1))
        self.assertEqual(rs.move_time, datetime.timedelta(2))

    def test__via_route(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.models.Route(name=rn, direction=d, start_station=s, end_station=s)
        r.save()
        rs = r.routestation_set.create(
            station=s,
            wait_time=datetime.timedelta(5),
            move_time=datetime.timedelta(6),
        )
        rs = trains.models.RouteStation.objects.filter(pk=rs.id).first()
        self.assertEqual(rs.route.name, rn)
        self.assertEqual(rs.station.name, sn)
        self.assertEqual(rs.wait_time, datetime.timedelta(5))
        self.assertEqual(rs.move_time, datetime.timedelta(6))

    def test__via_station(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.models.Route(name=rn, direction=d, start_station=s, end_station=s)
        r.save()
        rs = s.routestation_set.create(
            route=r,
            wait_time=datetime.timedelta(3),
            move_time=datetime.timedelta(4),
        )
        rs = trains.models.RouteStation.objects.filter(pk=rs.id).first()
        self.assertEqual(rs.route.name, rn)
        self.assertEqual(rs.station.name, sn)
        self.assertEqual(rs.wait_time, datetime.timedelta(3))
        self.assertEqual(rs.move_time, datetime.timedelta(4))


class WeekdayTests(django.test.TestCase):
    def test__conversion__int(self):
        wd = filter(
            lambda x: x[0] == trains.tools.Weekday.wednesday,
            trains.tools.Weekday.choices
        )[0][1]
        self.assertEqual(
            wd,
            trains.tools.Weekday(trains.tools.Weekday.wednesday)
        )

    def test__conversion__str(self):
        wd = filter(
            lambda x: x[0] == trains.tools.Weekday.monday,
            trains.tools.Weekday.choices
        )[0][1]
        self.assertEqual(
            wd,
            trains.tools.Weekday('0')
        )

    def test__conversion__invalid(self):
        self.assertEqual(trains.tools.Weekday(-1), None)
        self.assertEqual(trains.tools.Weekday('7'), None)
        self.assertEqual(trains.tools.Weekday('a'), None)


class TimetableModelTests(django.test.TestCase):
    def test__direct_creation(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.models.Route(name=rn, direction=d, start_station=s, end_station=s)
        r.save()
        tt = trains.models.Timetable(route=r, weekday=0, time=datetime.time(0, 1))
        tt.save()
        tt = trains.models.Timetable.objects.filter(pk=tt.id).first()
        self.assertEqual(tt.route.name, rn)
        self.assertEqual(tt.weekday, 0)
        self.assertEqual(tt.time, datetime.time(0, 1))

    def test__via_route(self):
        sn = str(uuid.uuid4())
        s = trains.models.Station(name=sn)
        s.save()
        dn = str(uuid.uuid4())
        d = trains.models.Direction(name=dn)
        d.save()
        rn = str(uuid.uuid4())
        r = trains.models.Route(name=rn, direction=d, start_station=s, end_station=s)
        r.save()
        tt = r.timetable_set.create(weekday=0, time=datetime.time(0, 1))
        tt.save()
        tt = trains.models.Timetable.objects.filter(pk=tt.id).first()
        self.assertEqual(tt.route.name, rn)
        self.assertEqual(tt.weekday, 0)
        self.assertEqual(tt.time, datetime.time(0, 1))
