# -*- coding: UTF-8 -*-

"""
Part of settings.py that contains Local settings. . Not standalone!
"""


import main_settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = main_settings.INSTALLED_APPS + ('django_jenkins',)

PROJECT_APPS = ('techblog',)

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
)


del main_settings
