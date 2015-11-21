from django.contrib import admin

from .models import Station, Direction, DirectionStation, Route


class DirectionStationInlite(admin.TabularInline):
    model = DirectionStation


class DirectionAdmin(admin.ModelAdmin):
    inlines = [DirectionStationInlite]


admin.site.register(Station)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Route)
