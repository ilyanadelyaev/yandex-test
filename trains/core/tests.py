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
    pass


class RouteModelTests(django.test.TestCase):
    pass


class DirectionModelTests(django.test.TestCase):
    pass
