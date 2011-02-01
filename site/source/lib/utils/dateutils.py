#!/usr/bin/python
# -*- coding: UTF-8 -*-

from log import logger
from datetime import datetime


SCHEDULE_RUS_MONTHS = {
   1:u'Января',
   2:u'Февраля',
   3:u'Марта',
   4:u'Апреля',
   5:u'Мая',
   6:u'Июня',
   7:u'Июля',
   8:u'Августа',
   9:u'Сентября',
   10:u'Октября',
   11:u'Ноября',
   12:u'Декабря',
}


def format_rus_schedule(start_date, end_date=None):
    '''
    >>> print format_rus_schedule(datetime(2010, 11, 1))
    1 Ноября
    >>> print format_rus_schedule(datetime(2010, 11, 1), datetime(2010, 11, 2))
    1-2 Ноября
    >>> print format_rus_schedule(datetime(2010, 1, 31), datetime(2010, 2, 1))
    31 Января - 1 Февраля
    '''
    if (end_date is None) or (end_date == start_date):
        dt = u'%d %s' % (
                           start_date.day,
                           SCHEDULE_RUS_MONTHS[start_date.month]
                           )
    elif start_date.month != end_date.month:
        dt = u'%d %s - %d %s' % (
                           start_date.day,
                           SCHEDULE_RUS_MONTHS[start_date.month],
                           end_date.day,
                           SCHEDULE_RUS_MONTHS[end_date.month])
    else: 
        dt = u'%d-%d %s' % (
                           start_date.day,
                           end_date.day,
                           SCHEDULE_RUS_MONTHS[start_date.month])
    return dt

if __name__ == '__main__':
    import doctest
    doctest.testmod()
