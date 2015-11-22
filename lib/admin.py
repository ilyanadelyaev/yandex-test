from django.contrib import admin

from . import models


class DirectionAdmin(admin.ModelAdmin):
    class __DirectionStationInlite(admin.TabularInline):
        model = models.DirectionStation
    inlines = [__DirectionStationInlite]


class RouteAdmin(admin.ModelAdmin):
    class __RouteStationsInline(admin.TabularInline):
        model = models.RouteStation
    class __TimetableInline(admin.TabularInline):
        model = models.Timetable
    inlines = [__RouteStationsInline, __TimetableInline]
    list_filter = ['direction']


admin.site.register(models.Station)
admin.site.register(models.Direction, DirectionAdmin)
admin.site.register(models.Route, RouteAdmin)
