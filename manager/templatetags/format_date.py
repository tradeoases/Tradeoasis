from django import template
from django.contrib.humanize.templatetags.humanize import naturalday

register = template.Library()

@register.filter(name='format_date')
def format_date(a):
    return naturalday(a)
    