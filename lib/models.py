from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.id)


class Direction(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.id)


class DirectionStation(models.Model):
    direction = models.ForeignKey(Direction)
    station = models.ForeignKey(Station)
    station_pos = models.PositiveSmallIntegerField()


class Route(models.Model):
    name = models.CharField(max_length=60)
    direction = models.ForeignKey(Direction)
    start_station = models.PositiveSmallIntegerField()
    end_station = models.PositiveSmallIntegerField()
    weekday = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.id)
