from django import template

register = template.Library()

@register.simple_tag
def corners(radius='8'):
    text = """
        <span class="outer-corners corner-radius-%s">
            <span class="corner-lt"></span>
            <span class="corner-rt"></span>
            <span class="corner-rb"></span>
            <span class="corner-lb"></span>
        </span>""" % radius
    return text