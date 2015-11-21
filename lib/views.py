from django.shortcuts import render
from django.views import generic
from django import forms

from .models import Station
from .models import Direction
from .models import Route


def index(request):
    return render(request, 'index.html', {})


class InvalidSearchConditions(Exception):
    pass


class SearchForm(forms.Form):
    start_station = forms.ModelChoiceField(queryset=Station.objects.all(), empty_label=None)
    end_station = forms.ModelChoiceField(queryset=Station.objects.all(), empty_label=None)


def search(request):
    form = SearchForm()
    return render(request, 'view/search.html', {
        'form': form,
    })


def results(request):
    try:
        start_station = request.GET['start_station']
        end_station = request.GET['end_station']
        if start_station == end_station:
            raise InvalidSearchConditions('start_station = end_station')
    except (KeyError, InvalidSearchConditions, Station.DoesNotExist) as ex:
        form = SearchForm()
        return render(request, 'view/search.html', {
            'error_message': str(ex),
            'form': form,
        })
    else:
        start_station = Station.objects.get(pk=start_station)
        end_station = Station.objects.get(pk=end_station)
        #
        return render(request, 'view/search_results.html', {
            'start_station': start_station,
            'end_station': end_station,
        })


class StationIndexView(generic.ListView):
    model = Station
    context_object_name = 'stations'
    template_name = 'view/stations_index.html'


class StationDetailView(generic.DetailView):
    model = Station
    template_name = 'view/stations_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StationDetailView, self).get_context_data(**kwargs)
        context['directionstation_list'] = self.object.directionstation_list()
        return context


class DirectionIndexView(generic.ListView):
    model = Direction
    context_object_name = 'directions'
    template_name = 'view/directions_index.html'


class DirectionDetailView(generic.DetailView):
    model = Direction
    template_name = 'view/directions_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DirectionDetailView, self).get_context_data(**kwargs)
        context['directionstation_list'] = self.object.directionstation_list()
        context['route_list'] = self.object.route_list()
        return context


class RouteIndexView(generic.ListView):
    model = Route
    context_object_name = 'routes'
    template_name = 'view/routes_index.html'


class RouteDetailView(generic.DetailView):
    model = Route
    template_name = 'view/routes_detail.html'
