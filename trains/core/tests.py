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


class RouteModelTests(django.test.TestCase):
    def test__has_fields(self):
        d = trains.core.models.Direction(name='D')
        d.save()
        r = trains.core.models.Route(name='R', direction=d)
        r.save()
        r = trains.core.models.Route.objects.get(pk=r.id)
        self.assertEqual(r.name, 'R')
        self.assertEqual(r.direction.name, 'D')


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
