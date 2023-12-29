from django import template

register = template.Library()


@register.simple_tag(name="get")
def get(value, arg):
    return value.get(arg)