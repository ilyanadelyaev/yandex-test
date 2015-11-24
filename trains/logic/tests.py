import datetime

import django.test

import trains.core.models
import trains.logic.search
import trains.logic.errors


class SearchLogicTests(django.test.TestCase):
    def setUp(self):
        #
        stations = [
            'Moscow',
            'Saint-Petersburg',
            'Helsinki',
            'International Space Station',
        ]
        for station in stations:
            trains.core.models.Station(name=station).save()
        #
        directions = [
            'Moscow - Saint-Petersburg',
            'Saint-Petersburg - Helsinki',
        ]
        for direction in directions:
            trains.core.models.Direction(name=direction).save()
        #
        directionstation = [
            ('Moscow - Saint-Petersburg', 'Moscow', 0),
            ('Moscow - Saint-Petersburg', 'Saint-Petersburg', 1),
            ('Saint-Petersburg - Helsinki', 'Saint-Petersburg', 0),
            ('Saint-Petersburg - Helsinki', 'Helsinki', 1),
        ]
        for direction, station, position in directionstation:
            trains.core.models.Direction.objects.filter(name=direction).first().directionstation_set.create(
                    station=trains.core.models.Station.objects.filter(name=station).first(),
                    position=position,
            )
        #
        routes = [
            ('Moscow - Saint-Petersburg', 'Moscow - Saint-Petersburg', 'Moscow', 'Saint-Petersburg'),
            ('Saint-Petersburg - Moscow', 'Moscow - Saint-Petersburg', 'Saint-Petersburg', 'Moscow'),
            ('Saint-Petersburg - Helsinki', 'Saint-Petersburg - Helsinki', 'Saint-Petersburg', 'Helsinki'),
            ('Helsinki - Saint-Petersburg', 'Saint-Petersburg - Helsinki', 'Helsinki', 'Saint-Petersburg'),
        ]
        for route, direction, start_station, end_station in routes:
            trains.core.models.Route(
                name=route,
                direction=trains.core.models.Direction.objects.filter(name=direction).first(),
                start_station=trains.core.models.Station.objects.filter(name=start_station).first(),
                end_station=trains.core.models.Station.objects.filter(name=end_station).first(),
            ).save()
        #
        routestation = [
            ('Moscow - Saint-Petersburg', 'Moscow', '00:00', '08:00'),
            ('Moscow - Saint-Petersburg', 'Saint-Petersburg', '00:00', '00:00'),

            ('Saint-Petersburg - Moscow', 'Saint-Petersburg', '00:00', '08:00'),
            ('Saint-Petersburg - Moscow', 'Moscow', '00:00', '00:00'),

            ('Saint-Petersburg - Helsinki', 'Saint-Petersburg', '00:00', '08:00'),
            ('Saint-Petersburg - Helsinki', 'Helsinki', '00:00', '00:00'),

            ('Helsinki - Saint-Petersburg', 'Helsinki', '00:00', '08:00'),
            ('Helsinki - Saint-Petersburg', 'Saint-Petersburg', '00:00', '00:00'),
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
            ('Moscow - Saint-Petersburg', 0, '08:00'),
            ('Saint-Petersburg - Moscow', 0, '08:00'),
            ('Saint-Petersburg - Helsinki', 0, '08:00'),
            ('Helsinki - Saint-Petersburg', 0, '08:00'),
        ]
        for route, weekday, time in timetable:
            time = datetime.datetime.strptime(time, '%H:%M')
            trains.core.models.Route.objects.filter(name=route).first().timetable_set.create(
                weekday=weekday,
                time=time,
            )

    def test__search__direct(self):
        s1 = trains.core.models.Station.objects.get(name='Saint-Petersburg')
        s2 = trains.core.models.Station.objects.get(name='Moscow')
        d = trains.core.models.Direction.objects.get(name='Moscow - Saint-Petersburg')
        r = trains.core.models.Route.objects.get(name='Saint-Petersburg - Moscow')
        tt = trains.core.models.Timetable.objects.filter(route=r).first()
        ret = trains.logic.search.search_routes(s1.id, s2.id, '11/16/2015', None)
        self.assertEqual(ret[0][0], s1)
        self.assertEqual(ret[0][1], s2)
        self.assertEqual(ret[0][2], d)
        self.assertEqual(ret[0][3][0][0], r)
        self.assertEqual(ret[0][3][0][1], tt.time)

    def test__search__one_hub_station(self):
        s1 = trains.core.models.Station.objects.get(name='Moscow')
        s2 = trains.core.models.Station.objects.get(name='Saint-Petersburg')
        s3 = trains.core.models.Station.objects.get(name='Helsinki')
        d1 = trains.core.models.Direction.objects.get(name='Moscow - Saint-Petersburg')
        d2 = trains.core.models.Direction.objects.get(name='Saint-Petersburg - Helsinki')
        r1 = trains.core.models.Route.objects.get(name='Moscow - Saint-Petersburg')
        r2 = trains.core.models.Route.objects.get(name='Saint-Petersburg - Helsinki')
        tt1 = trains.core.models.Timetable.objects.filter(route=r1).first()
        tt2 = trains.core.models.Timetable.objects.filter(route=r2).first()
        ret = trains.logic.search.search_routes(s1.id, s3.id, '11/16/2015', None)
        self.assertEqual(ret[0][0], s1)
        self.assertEqual(ret[0][1], s2)
        self.assertEqual(ret[0][2], d1)
        self.assertEqual(ret[0][3][0][0], r1)
        self.assertEqual(ret[0][3][0][1], tt1.time)
        self.assertEqual(ret[1][0], s2)
        self.assertEqual(ret[1][1], s3)
        self.assertEqual(ret[1][2], d2)
        self.assertEqual(ret[1][3][0][0], r2)
        self.assertEqual(ret[1][3][0][1], tt2.time)

    def test__search__invalid_arguments(self):
        with self.assertRaises(trains.logic.errors.InvalidSearchArguments):
            trains.logic.search.search_routes('a', 'b', '11/16/2015', None)

    def test__search__equal_start_end_stations(self):
        with self.assertRaises(trains.logic.errors.InvalidSearchArguments):
            trains.logic.search.search_routes(1, 1, '11/16/2015', None)

    def test__search__unbound_stations(self):
        s1 = trains.core.models.Station.objects.get(name='International Space Station')
        s2 = trains.core.models.Station.objects.get(name='Saint-Petersburg')
        with self.assertRaises(trains.logic.errors.UnboundedStations):
            trains.logic.search.search_routes(s1.id, s2.id, '11/16/2015', None)

    def test__search__empty_route(self):
        s1 = trains.core.models.Station.objects.get(name='Saint-Petersburg')
        s2 = trains.core.models.Station.objects.get(name='Moscow')
        ret = trains.logic.search.search_routes(s1.id, s2.id, '11/17/2015', None)
        self.assertFalse(ret[0][3])
