from django import template

register = template.Library()


@register.filter(name='spread')
def spread(value, arg):
    return value.split(arg)
