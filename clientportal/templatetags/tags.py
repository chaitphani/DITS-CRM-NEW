from django import template
register = template.Library()


@register.filter
def item_sum(items):
    return sum(items)

@register.filter
def item_division_100(items):
    return items/100