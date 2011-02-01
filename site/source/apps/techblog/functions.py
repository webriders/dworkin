#!/usr/bin/python
# -*- coding: UTF-8 -*-

# For code highlight
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.formatters import HtmlFormatter

def html_parser(value):
        value = re.sub('(?is)(<script[^>]*>.*?</script[^>]*>|<link[^>/]*/?>)', '', value).strip() # cleaning
        if value:
            formatter = HtmlFormatter(nowrap=True, lineseparator='<br/>', style=get_style_by_name('native'))
            def render_raw(match):
                lexer = get_lexer_by_name(match.groups()[0])
                return '<code class="highlight">%s</code>' % highlight(match.groups()[1], lexer, formatter)
            value = re.sub('(?is)<code[^>]*language="(\w+)"[^>]*>(.*?)</code[^>]*>', render_raw, value)
        return value

def int2bin(num):
    res = []
    while num:
        res.append(num % 2)
        num = num / 2
    return res

def binary_date(date):
    res = '<div class="day-line">'
    for i in int2bin(date.day):
        res += '<span class="bit-%d"></span>' % i
    res += '</div><div class="month-line">'
    for i in int2bin(date.month):
        res += '<span class="bit-%d"></span>' % i
    res += '</div><div class="year-line">'
    for i in int2bin(date.year % 100):
        res += '<span class="bit-%d"></span>' % i
    res += '</div>'
    return res

def formatted_date(date):
    res = u"""
    <span class="date-day">%d</span>
    <span class="date-month">%s</span>
    <span class="date-year">%d</span>
    <span class="date-time">%s</span>
    """ % (
            date.day,
            [u'Янв', u'Фев', u'Мар', u'Апр', u'Май', u'Июн', u'Июл', u'Авг', u'Сен', u'Окт', u'Ноя', u'Дек'][date.month - 1],
            date.year,
            date.time().strftime('%H:%M')
            )
    return res
