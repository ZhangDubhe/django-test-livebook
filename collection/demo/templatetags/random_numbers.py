import random
from django import template

register = template.Library()

@register.simple_tag
def randomInt(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)