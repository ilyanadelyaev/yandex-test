import django.shortcuts
import django.forms


def search(request):
    return django.shortcuts.render(request, 'www/search.html')


def stations_list(request):
    return django.shortcuts.render(request, 'www/stations_list.html')


def station(request, pk):
    return django.shortcuts.render(request, 'www/station.html', {'pk': pk})


def directions_list(request):
    return django.shortcuts.render(request, 'www/directions_list.html')


def direction(request, pk):
    return django.shortcuts.render(request, 'www/direction.html', {'pk': pk})


def routes_list(request):
    return django.shortcuts.render(request, 'www/routes_list.html')


def route(request, pk):
    return django.shortcuts.render(request, 'www/route.html', {'pk': pk})
