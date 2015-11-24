import django.shortcuts
import django.forms


class SearchForm(django.forms.Form):
    start_station = django.forms.ChoiceField()
    end_station = django.forms.ChoiceField()
    weekday = django.forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['start_station'].widget.attrs['class'] = 'form-control'
        self.fields['end_station'].widget.attrs['class'] = 'form-control'
        self.fields['weekday'].widget.attrs['class'] = 'form-control'


def search(request):
    form = SearchForm()
    return django.shortcuts.render(request, 'www/search.html', {'form': form})


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
