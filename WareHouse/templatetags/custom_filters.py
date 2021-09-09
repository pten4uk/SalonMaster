from django import template

register = template.Library()


@register.filter(name='divider')
def divider(value, div):
    value = value // div
    return value


@register.filter(name='reminder')
def reminder(value, div):
    value = value % div
    return value
