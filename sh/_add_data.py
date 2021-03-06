import datetime

import trains.models


print None  # make new line


stations = [
    'Moscow',
    'Saint-Petersburg',
    'Novosibirsk',
    'Tver',
    'Bologoe',
    'Minsk',
    'Helsinki',
    'Prague',
    'Berlin',
    'Dresden',
    'Paris',
    'International Space Station'
]

for station in stations:
    print 'Add station "{}"'.format(station)
    trains.models.Station(name=station).save()


print '-' * 40


directions = [
    'Moscow - Saint-Petersburg',
    'Moscow - Novosibirsk',
    'Moscow - Minsk',
    'Saint-Petersburg - Helsinki',
    'Minsk - Prague',
    'Prague - Helsinki',
    'Prague - Berlin',
    'Berlin - Paris',
]

for direction in directions:
    print 'Add directions "{}"'.format(direction)
    trains.models.Direction(name=direction).save()


print '-' * 40


directionstation = [
    ('Moscow - Saint-Petersburg', 'Moscow', 0),
    ('Moscow - Saint-Petersburg', 'Tver', 1),
    ('Moscow - Saint-Petersburg', 'Bologoe', 2),
    ('Moscow - Saint-Petersburg', 'Saint-Petersburg', 3),
    ('Moscow - Novosibirsk', 'Moscow', 0),
    ('Moscow - Novosibirsk', 'Novosibirsk', 1),
    ('Moscow - Minsk', 'Moscow', 0),
    ('Moscow - Minsk', 'Minsk', 1),
    ('Saint-Petersburg - Helsinki', 'Saint-Petersburg', 0),
    ('Saint-Petersburg - Helsinki', 'Helsinki', 1),
    ('Minsk - Prague', 'Minsk', 0),
    ('Minsk - Prague', 'Prague', 1),
    ('Prague - Helsinki', 'Prague', 0),
    ('Prague - Helsinki', 'Helsinki', 1),
    ('Prague - Berlin', 'Prague', 0),
    ('Prague - Berlin', 'Dresden', 1),
    ('Prague - Berlin', 'Berlin', 2),
    ('Berlin - Paris', 'Berlin', 0),
    ('Berlin - Paris', 'Paris', 1),
]

for direction, station, position in directionstation:
    print 'Add station "{}" to direction "()" with pos: "{}"'.format(station, direction, position)
    trains.models.Direction.objects.filter(name=direction).first().directionstation_set.create(
            station=trains.models.Station.objects.filter(name=station).first(),
            position=position,
    )


print '-' * 40


routes = [
    ('Moscow - Saint-Petersburg', 'Moscow - Saint-Petersburg', 'Moscow', 'Saint-Petersburg'),
    ('Saint-Petersburg - Moscow', 'Moscow - Saint-Petersburg', 'Saint-Petersburg', 'Moscow'),
    ('Moscow - Saint-Petersburg - EXPRESS', 'Moscow - Saint-Petersburg', 'Moscow', 'Saint-Petersburg'),
    ('Saint-Petersburg - Moscow - EXPRESS', 'Moscow - Saint-Petersburg', 'Saint-Petersburg', 'Moscow'),
    ('Moscow - Novosibirsk', 'Moscow - Novosibirsk', 'Moscow', 'Novosibirsk'),
    ('Novosibirsk - Moscow', 'Moscow - Novosibirsk', 'Novosibirsk', 'Moscow'),
    ('Moscow - Minsk', 'Moscow - Minsk', 'Moscow', 'Minsk'),
    ('Minsk - Moscow', 'Moscow - Minsk', 'Minsk', 'Moscow'),
    ('Saint-Petersburg - Helsinki', 'Saint-Petersburg - Helsinki', 'Saint-Petersburg', 'Helsinki'),
    ('Helsinki - Saint-Petersburg', 'Saint-Petersburg - Helsinki', 'Helsinki', 'Saint-Petersburg'),
    ('Minsk - Prague', 'Minsk - Prague', 'Minsk', 'Prague'),
    ('Prague - Minsk', 'Minsk - Prague', 'Prague', 'Minsk'),
    ('Prague - Helsinki', 'Prague - Helsinki', 'Prague', 'Helsinki'),
    ('Helsinki - Prague', 'Prague - Helsinki', 'Helsinki', 'Prague'),
    ('Prague - Berlin', 'Prague - Berlin', 'Prague', 'Berlin'),
    ('Berlin - Prague', 'Prague - Berlin', 'Berlin', 'Prague'),
    ('Prague - Berlin - EXPRESS', 'Prague - Berlin', 'Prague', 'Berlin'),
    ('Berlin - Prague - EXPRESS', 'Prague - Berlin', 'Berlin', 'Prague'),
    ('Berlin - Paris', 'Berlin - Paris', 'Berlin', 'Paris'),
    ('Paris - Berlin', 'Berlin - Paris', 'Paris', 'Berlin'),
]

for route, direction, start_station, end_station in routes:
    print 'Add route "{}" for direction "{}" with: start_station: "{}", end_station: "{}"'.format(
        route, direction, start_station, end_station)
    trains.models.Route(
        name=route,
        direction=trains.models.Direction.objects.filter(name=direction).first(),
        start_station=trains.models.Station.objects.filter(name=start_station).first(),
        end_station=trains.models.Station.objects.filter(name=end_station).first(),
    ).save()


print '-' * 40


routestation = [
    ('Moscow - Saint-Petersburg', 'Moscow', '00:00', '04:00'),
    ('Moscow - Saint-Petersburg', 'Tver', '00:10', '03:00'),
    ('Moscow - Saint-Petersburg', 'Bologoe', '00:05', '01:00'),
    ('Moscow - Saint-Petersburg', 'Saint-Petersburg', '00:00', '00:00'),

    ('Saint-Petersburg - Moscow', 'Saint-Petersburg', '00:00', '01:00'),
    ('Saint-Petersburg - Moscow', 'Bologoe', '00:05', '03:00'),
    ('Saint-Petersburg - Moscow', 'Tver', '00:10', '04:00'),
    ('Saint-Petersburg - Moscow', 'Moscow', '00:00', '00:00'),

    ('Moscow - Saint-Petersburg - EXPRESS', 'Moscow', '00:00', '07:00'),
    ('Moscow - Saint-Petersburg - EXPRESS', 'Saint-Petersburg', '00:00', '00:00'),

    ('Saint-Petersburg - Moscow - EXPRESS', 'Saint-Petersburg', '00:00', '07:00'),
    ('Saint-Petersburg - Moscow - EXPRESS', 'Moscow', '00:00', '00:00'),

    ('Moscow - Novosibirsk', 'Moscow', '00:00', '23:00'),
    ('Moscow - Novosibirsk', 'Novosibirsk', '00:00', '00:00'),

    ('Novosibirsk - Moscow', 'Novosibirsk', '00:00', '23:00'),
    ('Novosibirsk - Moscow', 'Moscow', '00:00', '00:00'),

    ('Moscow - Minsk', 'Moscow', '00:00', '03:00'),
    ('Moscow - Minsk', 'Minsk', '00:00', '00:00'),

    ('Minsk - Moscow', 'Minsk', '00:00', '03:00'),
    ('Minsk - Moscow', 'Moscow', '00:00', '00:00'),

    ('Saint-Petersburg - Helsinki', 'Saint-Petersburg', '00:00', '08:00'),
    ('Saint-Petersburg - Helsinki', 'Helsinki', '00:00', '00:00'),

    ('Helsinki - Saint-Petersburg', 'Helsinki', '00:00', '08:00'),
    ('Helsinki - Saint-Petersburg', 'Saint-Petersburg', '00:00', '00:00'),

    ('Minsk - Prague', 'Minsk', '00:00', '05:00'),
    ('Minsk - Prague', 'Prague', '00:00', '00:00'),

    ('Prague - Minsk', 'Prague', '00:00', '05:00'),
    ('Prague - Minsk', 'Minsk', '00:00', '00:00'),

    ('Prague - Helsinki', 'Prague', '00:00', '06:00'),
    ('Prague - Helsinki', 'Helsinki', '00:00', '00:00'),

    ('Helsinki - Prague', 'Helsinki', '00:00', '06:00'),
    ('Helsinki - Prague', 'Prague', '00:00', '00:00'),

    ('Prague - Berlin', 'Prague', '00:00', '01:30'),
    ('Prague - Berlin', 'Dresden', '00:05', '01:00'),
    ('Prague - Berlin', 'Berlin', '00:00', '00:00'),

    ('Berlin - Prague', 'Berlin', '00:00', '01:00'),
    ('Berlin - Prague', 'Dresden', '00:05', '01:30'),
    ('Berlin - Prague', 'Prague', '00:00', '00:00'),

    ('Prague - Berlin - EXPRESS', 'Prague', '00:00', '02:00'),
    ('Prague - Berlin - EXPRESS', 'Berlin', '00:00', '00:00'),

    ('Berlin - Prague - EXPRESS', 'Berlin', '00:00', '02:00'),
    ('Berlin - Prague - EXPRESS', 'Prague', '00:00', '00:00'),

    ('Berlin - Paris', 'Berlin', '00:00', '03:00'),
    ('Berlin - Paris', 'Paris', '00:00', '00:00'),

    ('Paris - Berlin', 'Paris', '00:00', '03:00'),
    ('Paris - Berlin', 'Berlin', '00:00', '00:00'),
]

for route, station, wait_time, move_time in routestation:
    print 'Add station "{}" to route "{}" with pos: "{}", start: "{}", end: "{}"'.format(
        station, route, position, wait_time, move_time)
    wait_time = datetime.datetime.strptime(wait_time, '%H:%M')
    wait_time = datetime.timedelta(hours=wait_time.hour, minutes=wait_time.minute)
    move_time = datetime.datetime.strptime(move_time, '%H:%M')
    move_time = datetime.timedelta(hours=move_time.hour, minutes=move_time.minute)
    trains.models.Route.objects.filter(name=route).first().routestation_set.create(
        station=trains.models.Station.objects.filter(name=station).first(),
        wait_time=wait_time,
        move_time=move_time,
    )


print '-' * 40

timetable = [
    ('Moscow - Saint-Petersburg', '08:00'),
    ('Saint-Petersburg - Moscow', '08:00'),
    ('Moscow - Saint-Petersburg - EXPRESS', '08:00'),
    ('Saint-Petersburg - Moscow - EXPRESS', '08:00'),
    ('Moscow - Novosibirsk', '08:00'),
    ('Novosibirsk - Moscow', '08:00'),
    ('Moscow - Minsk', '08:00'),
    ('Minsk - Moscow', '08:00'),
    ('Saint-Petersburg - Helsinki', '08:00'),
    ('Helsinki - Saint-Petersburg', '08:00'),
    ('Minsk - Prague', '08:00'),
    ('Prague - Minsk', '08:00'),
    ('Prague - Helsinki', '08:00'),
    ('Helsinki - Prague', '08:00'),
    ('Prague - Berlin', '08:00'),
    ('Berlin - Prague', '08:00'),
    ('Prague - Berlin - EXPRESS', '08:00'),
    ('Berlin - Prague - EXPRESS', '08:00'),
    ('Berlin - Paris', '08:00'),
    ('Paris - Berlin', '08:00'),
]

for route, time in timetable:
    print 'Timetable for route "{}", time: "{}"'.format(route, time)
    time = datetime.datetime.strptime(time, '%H:%M')
    for weekday in xrange(7):
        trains.models.Route.objects.filter(name=route).first().timetable_set.create(
            weekday=weekday,
            time=time,
        )
