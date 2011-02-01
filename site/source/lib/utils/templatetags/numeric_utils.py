from django.template import Library
import random

register = Library()

@register.simple_tag
def random_from_list(items=''):
    l = list(i.strip() for i in items.split(','))
    if l:
        l = random.choice(l)
    return l