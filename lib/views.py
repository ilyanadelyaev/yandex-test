from django.shortcuts import render
from django.views import generic
from django import forms

from .models import Station
from .models import Direction
from .models import Route

from . import logic
from . import tools


class SearchView(object):
    class InvalidSearchConditions(Exception):
        pass

    class SearchForm(forms.Form):
        start_station = forms.ModelChoiceField(queryset=Station.objects.all(),
            empty_label=None)
        end_station = forms.ModelChoiceField(queryset=Station.objects.all(),
            empty_label=None)
        weekday = forms.ChoiceField(choices=tools.Weekday.choices)

        def __init__(self, *args, **kwargs):
            super(SearchView.SearchForm, self).__init__(*args, **kwargs)
            self.fields['start_station'].widget.attrs['class'] = 'form-control'
            self.fields['end_station'].widget.attrs['class'] = 'form-control'
            self.fields['weekday'].widget.attrs['class'] = 'form-control'

    @classmethod
    def search(cls, request):
        form = cls.SearchForm()
        return render(request, 'view/search.html', {
            'form': form,
        })

    @classmethod
    def search_results(cls, request):
        try:
            start_station = request.GET['start_station']
            end_station = request.GET['end_station']
            if start_station == end_station:
                raise cls.InvalidSearchConditions('start_station = end_station')
            weekday = request.GET['weekday']
        except (KeyError, cls.InvalidSearchConditions, Station.DoesNotExist) as ex:
            form = cls.SearchForm()
            return render(request, 'view/search.html', {
                'error_message': str(ex),
                'form': form,
            })
        else:
            start_station = Station.objects.get(pk=start_station)
            end_station = Station.objects.get(pk=end_station)
            #
            route = logic.search_routes(start_station.id, end_station.id, weekday)
            #
            return render(request, 'view/search_results.html', {
                'start_station': start_station,
                'end_station': end_station,
                'weekday': weekday,
                'route': route,
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
        context['routestation_list'] = self.object.routestation_list()
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

    def get_context_data(self, **kwargs):
        context = super(RouteDetailView, self).get_context_data(**kwargs)
        context['routestation_list'] = self.object.routestation_list()
        context['timetable_list'] = self.object.timetable_list()
        return context
