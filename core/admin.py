import django.contrib.admin

import core.models


class DirectionAdmin(django.contrib.admin.ModelAdmin):
    class __DirectionStationInlite(django.contrib.admin.TabularInline):
        model = core.models.DirectionStation
    inlines = [__DirectionStationInlite]


class RouteAdmin(django.contrib.admin.ModelAdmin):
    class __RouteStationsInline(django.contrib.admin.TabularInline):
        model = core.models.RouteStation
    class __TimetableInline(django.contrib.admin.TabularInline):
        model = core.models.Timetable
    inlines = [__RouteStationsInline, __TimetableInline]
    list_filter = ['direction']


django.contrib.admin.site.register(core.models.Station)
django.contrib.admin.site.register(core.models.Direction, DirectionAdmin)
django.contrib.admin.site.register(core.models.Route, RouteAdmin)
