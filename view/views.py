import django.forms
import django.views.generic
import django.shortcuts

import core.models
import core.logic
import lib.tools


class SearchView(object):
    class InvalidSearchConditions(Exception):
        pass

    class SearchForm(django.forms.Form):
        start_station = django.forms.ModelChoiceField(queryset=core.models.Station.objects.all(),
            empty_label=None)
        end_station = django.forms.ModelChoiceField(queryset=core.models.Station.objects.all(),
            empty_label=None)
        weekday = django.forms.ChoiceField(choices=lib.tools.Weekday.choices)

        def __init__(self, *args, **kwargs):
            super(SearchView.SearchForm, self).__init__(*args, **kwargs)
            self.fields['start_station'].widget.attrs['class'] = 'form-control'
            self.fields['end_station'].widget.attrs['class'] = 'form-control'
            self.fields['weekday'].widget.attrs['class'] = 'form-control'

    @classmethod
    def search(cls, request):
        form = cls.SearchForm()
        return django.shortcuts.render(request, 'view/search.html', {
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
        except (KeyError, cls.InvalidSearchConditions, core.models.Station.DoesNotExist) as ex:
            form = cls.SearchForm()
            return django.shortcuts.render(request, 'view/search.html', {
                'error_message': str(ex),
                'form': form,
            })
        else:
            start_station = core.models.Station.objects.get(pk=start_station)
            end_station = core.models.Station.objects.get(pk=end_station)
            #
            route = core.logic.search_routes(start_station.id, end_station.id, weekday)
            #
            return django.shortcuts.render(request, 'view/search_results.html', {
                'start_station': start_station,
                'end_station': end_station,
                'weekday': weekday,
                'route': route,
            })


class StationIndexView(django.views.generic.ListView):
    model = core.models.Station
    context_object_name = 'stations'
    template_name = 'view/stations_index.html'


class StationDetailView(django.views.generic.DetailView):
    model = core.models.Station
    template_name = 'view/stations_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StationDetailView, self).get_context_data(**kwargs)
        context['directionstation_list'] = self.object.directionstation_list()
        context['routestation_list'] = self.object.routestation_list()
        return context


class DirectionIndexView(django.views.generic.ListView):
    model = core.models.Direction
    context_object_name = 'directions'
    template_name = 'view/directions_index.html'


class DirectionDetailView(django.views.generic.DetailView):
    model = core.models.Direction
    template_name = 'view/directions_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DirectionDetailView, self).get_context_data(**kwargs)
        context['directionstation_list'] = self.object.directionstation_list()
        context['route_list'] = self.object.route_list()
        return context


class RouteIndexView(django.views.generic.ListView):
    model = core.models.Route
    context_object_name = 'routes'
    template_name = 'view/routes_index.html'


class RouteDetailView(django.views.generic.DetailView):
    model = core.models.Route
    template_name = 'view/routes_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RouteDetailView, self).get_context_data(**kwargs)
        context['routestation_list'] = self.object.routestation_list()
        context['timetable_list'] = self.object.timetable_list()
        return context
