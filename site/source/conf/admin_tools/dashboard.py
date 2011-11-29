#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.dashboard.modules import AppList, ModelList, LinkList, Group, DashboardModule, RecentActions

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for code.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.columns = 2
        self.children.append(ModelList(
            title = u'Blog',
            deletable=False,
            draggable=False,
            collapsible=True,
            include_list=('techblog', 'taggit', 'threadedcomments',)
        ))
        self.children.append(ModelList(
            title = u'Authors and Groups',
            deletable=False,
            draggable=False,
            collapsible=True,
            include_list=('django.contrib.auth', 'techblog.models.UserProfile')
        ))
        self.children.append(modules.RecentActions(
            title=u'Recent changes',
            draggable=False,
            deletable=False,
            collapsible=True
        ))

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for code.
    """
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)
        # we disable title because its redundant with the model list module
        self.title = ''
        self.columns = 1
        # append a model list module
        from django.utils.safestring import mark_safe
        self.children.append(modules.ModelList(
            title=_(self.app_title),
            include_list=self.models,
            draggable=False,
            deletable=False,
            collapsible=False,
            pre_content=mark_safe( (u'Here you can edit only <b>part of your site: Module %s </b>. ' +
                                    u'To see the hole picture - <a href="%s">back to Main</a>') % (_(self.app_title), reverse('admin:index'))),
        ))
        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=u'Recent changes in this module',
            draggable=False,
            deletable=False,
            collapsible=False,
            include_list=self.get_app_content_types(),
        ))
