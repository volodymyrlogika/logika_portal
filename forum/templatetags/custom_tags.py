from django import template

register =  template.Library()

@register.filter(name="endswith")

def endswith(value, arg):
    return value.lower().endswith(arg.lower())

def range(number):
    context = range(number)
    return context