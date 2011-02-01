#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import items, Menu
from django.contrib.admin.models import LogEntry

# to activate your custom menu add the following to your settings.py:
from django.utils.safestring import mark_safe


class CustomMenu(Menu):
    """
    Custom Menu for Ukrros admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children.append(items.MenuItem(
            title=u'Главная',
            url=reverse('admin:index')
        ))
        self.children.append(items.Bookmarks(title=u'Закладки'))
        self.children.append(items.MenuItem(
            title=u'Перейти к сайту',
            url='/'
        ))


    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
