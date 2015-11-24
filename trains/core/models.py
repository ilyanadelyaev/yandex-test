import django.db


class Station(django.db.models.Model):
    name = django.db.models.CharField(max_length=30)

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.id)

    #TODO: drop me
    def directionstation_list(self):
        return self.directionstation_set.all()

    def routestation_list(self):
        return self.routestation_set.all()


class Direction(django.db.models.Model):
    name = django.db.models.CharField(max_length=60)

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.id)

    def directionstation_list(self):
        return self.directionstation_set.all()

    def route_list(self):
        return self.route_set.all()


class DirectionStation(django.db.models.Model):
    direction = django.db.models.ForeignKey(Direction)
    station = django.db.models.ForeignKey(Station)
    position = django.db.models.PositiveSmallIntegerField()


class Route(django.db.models.Model):
    name = django.db.models.CharField(max_length=60)
    direction = django.db.models.ForeignKey(Direction)

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.id)

    def routestation_list(self):
        return self.routestation_set.all()

    def timetable_list(self):
        return self.timetable_set.all()


class RouteStation(django.db.models.Model):
    route = django.db.models.ForeignKey(Route)
    station = django.db.models.ForeignKey(Station)
    position = django.db.models.PositiveSmallIntegerField()
    wait_time = django.db.models.DurationField()
    move_time = django.db.models.DurationField()

    def __unicode__(self):
        return '{} - {} - {} [{}]'.format(self.station, self.route, self.position, self.id)


class Weekday(object):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

    choices = (
        (monday, 'Monday'),
        (tuesday, 'Tuesday'),
        (wednesday, 'Wednesday'),
        (thursday, 'Thursday'),
        (friday, 'Friday'),
        (saturday, 'Saturday'),
        (sunday, 'Sunday'),
    )

    class __Meta(type):
        def __call__(cls, wd):
            return cls._to_str(wd)
    __metaclass__ = __Meta

    __choices = dict(choices)

    @classmethod
    def _to_str(cls, wd):
        try:
            wd = int(wd)
        except ValueError:
            return ''
        return cls.__choices.get(wd, '')


class Timetable(django.db.models.Model):
    route = django.db.models.ForeignKey(Route)
    weekday = django.db.models.PositiveSmallIntegerField(choices=Weekday.choices)
    time = django.db.models.TimeField()

    def __unicode__(self):
        return '{} - {} : {} [{}]'.format(self.route, self.weekday, self.time, self.id)
