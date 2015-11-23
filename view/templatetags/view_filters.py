import django.template

import lib.tools


register = django.template.Library()


@register.filter(name='weekday')
def weekday(value):
    return lib.tools.Weekday(int(value))
