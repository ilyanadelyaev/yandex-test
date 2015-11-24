import datetime

import django.test

import trains.core.models


class StationModelTests(django.test.TestCase):
    def test__has_fields(self):
        s = trains.core.models.Station(name='S')
        s.save()
        s = trains.core.models.Station.objects.get(pk=s.id)
        self.assertEqual(s.name, 'S')

    def test__directionstation_list(self):
        d = trains.core.models.Direction(name='D')
        d.save()
        s = trains.core.models.Station(name='S')
        s.save()
        self.assertEqual(len(s.directionstation_list()), 0)
        s.directionstation_set.create(direction=d, position=1)
        self.assertEqual(len(s.directionstation_list()), 1)
        ll = set(((i.direction.id, i.direction.name, i.position) for i in s.directionstation_list()))
        self.assertIn((d.id, d.name, 1), ll)


class DirectionModelTests(django.test.TestCase):
    def test__has_fields(self):
        d = trains.core.models.Direction(name='D')
        d.save()
        d = trains.core.models.Direction.objects.get(pk=d.id)
        self.assertEqual(d.name, 'D')


class DirectionStationModelTests(django.test.TestCase):
    def test__direct_creation(self):
        s = trains.core.models.Station(name='S')
        s.save()
        d = trains.core.models.Direction(name='D')
        d.save()
        ds = trains.core.models.DirectionStation(
            direction=d, station=s, position=4)
        ds.save()
        ds = trains.core.models.DirectionStation.objects.filter(pk=ds.id).first()
        self.assertEqual(ds.direction.id, d.id)
        self.assertEqual(ds.station.id, s.id)
        self.assertEqual(ds.position, 4)

    def test__via_direction(self):
        s = trains.core.models.Station(name='S')
        s.save()
        d = trains.core.models.Direction(name='D')
        d.save()
        ds = d.directionstation_set.create(station=s, position=5)
        ds = trains.core.models.DirectionStation.objects.filter(
            pk=ds.id).first()
        self.assertEqual(ds.direction.id, d.id)
        self.assertEqual(ds.station.id, s.id)
        self.assertEqual(ds.position, 5)

    def test__via_station(self):
        s = trains.core.models.Station(name='S')
        s.save()
        d = trains.core.models.Direction(name='D')
        d.save()
        ds = s.directionstation_set.create(direction=d, position=6)
        ds = trains.core.models.DirectionStation.objects.filter(
            pk=ds.id).first()
        self.assertEqual(ds.direction.id, d.id)
        self.assertEqual(ds.station.id, s.id)
        self.assertEqual(ds.position, 6)


class RouteModelTests(django.test.TestCase):
    def test__has_fields(self):
        d = trains.core.models.Direction(name='D')
        d.save()
        r = trains.core.models.Route(name='R', direction=d)
        r.save()
        r = trains.core.models.Route.objects.get(pk=r.id)
        self.assertEqual(r.name, 'R')
        self.assertEqual(r.direction.name, 'D')


class RouteStationModelTests(django.test.TestCase):
    def test__direct_creation(self):
        s = trains.core.models.Station(name='S')
        s.save()
        d = trains.core.models.Direction(name='D')
        d.save()
        r = trains.core.models.Route(name='R', direction=d)
        r.save()
        rs = trains.core.models.RouteStation(
            route=r, station=s, position=10,
            wait_time=datetime.timedelta(1),
            move_time=datetime.timedelta(2),
        )
        rs.save()
        rs = trains.core.models.RouteStation.objects.filter(pk=rs.id).first()
        self.assertEqual(rs.route.id, r.id)
        self.assertEqual(rs.station.id, s.id)
        self.assertEqual(rs.position, 10)
        self.assertEqual(rs.wait_time, datetime.timedelta(1))
        self.assertEqual(rs.move_time, datetime.timedelta(2))

    def test__via_route(self):
        s = trains.core.models.Station(name='S')
        s.save()
        d = trains.core.models.Direction(name='D')
        d.save()
        r = trains.core.models.Route(name='R', direction=d)
        r.save()
        rs = r.routestation_set.create(
            station=s, position=12,
            wait_time=datetime.timedelta(5),
            move_time=datetime.timedelta(6),
        )
        rs = trains.core.models.RouteStation.objects.filter(pk=rs.id).first()
        self.assertEqual(rs.route.id, r.id)
        self.assertEqual(rs.station.id, s.id)
        self.assertEqual(rs.position, 12)
        self.assertEqual(rs.wait_time, datetime.timedelta(5))
        self.assertEqual(rs.move_time, datetime.timedelta(6))

    def test__via_station(self):
        s = trains.core.models.Station(name='S')
        s.save()
        d = trains.core.models.Direction(name='D')
        d.save()
        r = trains.core.models.Route(name='R', direction=d)
        r.save()
        rs = s.routestation_set.create(
            route=r, position=11,
            wait_time=datetime.timedelta(3),
            move_time=datetime.timedelta(4),
        )
        rs = trains.core.models.RouteStation.objects.filter(pk=rs.id).first()
        self.assertEqual(rs.route.id, r.id)
        self.assertEqual(rs.station.id, s.id)
        self.assertEqual(rs.position, 11)
        self.assertEqual(rs.wait_time, datetime.timedelta(3))
        self.assertEqual(rs.move_time, datetime.timedelta(4))


class WeekdayTests(django.test.TestCase):
    def test__conversion__int(self):
        wd = filter(
            lambda x: x[0] == trains.core.models.Weekday.wednesday,
            trains.core.models.Weekday.choices
        )[0][1]
        self.assertEqual(
            wd,
            trains.core.models.Weekday(trains.core.models.Weekday.wednesday)
        )

    def test__conversion__str(self):
        wd = filter(
            lambda x: x[0] == trains.core.models.Weekday.monday,
            trains.core.models.Weekday.choices
        )[0][1]
        self.assertEqual(
            wd,
            trains.core.models.Weekday('0')
        )

    def test__conversion__invalid(self):
        self.assertEqual(trains.core.models.Weekday(-1), '')
        self.assertEqual(trains.core.models.Weekday('7'), '')
        self.assertEqual(trains.core.models.Weekday('a'), '')


class TimetableModelTests(django.test.TestCase):
    def test__direct_creation(self):
        d = trains.core.models.Direction(name='D')
        d.save()
        r = trains.core.models.Route(name='R', direction=d)
        r.save()
        tt = trains.core.models.Timetable(route=r, weekday=0, time=datetime.time(0, 1))
        tt.save()
        tt = trains.core.models.Timetable.objects.filter(pk=tt.id).first()
        self.assertEqual(tt.route.id, r.id)
        self.assertEqual(tt.weekday, 0)
        self.assertEqual(tt.time, datetime.time(0, 1))

    def test__via_route(self):
        d = trains.core.models.Direction(name='D')
        d.save()
        r = trains.core.models.Route(name='R', direction=d)
        r.save()
        tt = r.timetable_set.create(weekday=0, time=datetime.time(0, 1))
        tt.save()
        tt = trains.core.models.Timetable.objects.filter(pk=tt.id).first()
        self.assertEqual(tt.route.id, r.id)
        self.assertEqual(tt.weekday, 0)
        self.assertEqual(tt.time, datetime.time(0, 1))
