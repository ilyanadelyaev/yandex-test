from django import template

from .. import tools


register = template.Library()


@register.filter(name='weekday')
def weekday(value):
    return tools.Weekday(int(value))
