from django.db import models

from .tools import Weekday


class Station(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.id)

    def directionstation_list(self):
        return self.directionstation_set.all()

    def routestation_list(self):
        return self.routestation_set.all()


class Direction(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.id)

    def directionstation_list(self):
        return self.directionstation_set.all()

    def route_list(self):
        return self.route_set.all()


class DirectionStation(models.Model):
    direction = models.ForeignKey(Direction)
    station = models.ForeignKey(Station)
    position = models.PositiveSmallIntegerField()


class Route(models.Model):
    name = models.CharField(max_length=60)
    direction = models.ForeignKey(Direction)

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.id)

    def routestation_list(self):
        return self.routestation_set.all()

    def timetable_list(self):
        return self.timetable_set.all()


class RouteStation(models.Model):
    route = models.ForeignKey(Route)
    station = models.ForeignKey(Station)
    position = models.PositiveSmallIntegerField()
    wait_time = models.DurationField()
    move_time = models.DurationField()

    def __unicode__(self):
        return '{} - {} - {} [{}]'.format(self.station, self.route, self.position, self.id)


class Timetable(models.Model):
    route = models.ForeignKey(Route)
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    time = models.TimeField()

    def __unicode__(self):
        return '{} - {} : {} [{}]'.format(self.route, self.weekday, self.time, self.id)
