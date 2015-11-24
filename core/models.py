import django.db

import lib.tools


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


class Timetable(django.db.models.Model):
    route = django.db.models.ForeignKey(Route)
    weekday = django.db.models.PositiveSmallIntegerField(choices=lib.tools.Weekday.choices)
    time = django.db.models.TimeField()

    def __unicode__(self):
        return '{} - {} : {} [{}]'.format(self.route, self.weekday, self.time, self.id)
