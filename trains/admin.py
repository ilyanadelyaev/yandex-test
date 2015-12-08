import django.contrib.admin

import trains.models


class DirectionAdmin(django.contrib.admin.ModelAdmin):
    class __DirectionStationInlite(django.contrib.admin.TabularInline):
        model = trains.models.DirectionStation

    inlines = [__DirectionStationInlite]


class RouteAdmin(django.contrib.admin.ModelAdmin):
    class __RouteStationsInline(django.contrib.admin.TabularInline):
        model = trains.models.RouteStation

    class __TimetableInline(django.contrib.admin.TabularInline):
        model = trains.models.Timetable

    inlines = [__RouteStationsInline, __TimetableInline]
    list_filter = ['direction']


django.contrib.admin.site.register(trains.models.Station)
django.contrib.admin.site.register(trains.models.Direction, DirectionAdmin)
django.contrib.admin.site.register(trains.models.Route, RouteAdmin)
