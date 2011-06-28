#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Django settings for project.
import os
import sys

# Debug settings
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Force removal of fastcgi script name from URL
FORCE_SCRIPT_NAME=""

# We are in "project/trunk/code/" folder. We need to get PROJECT_ROOT
PROJECT_ROOT = os.path.abspath('..')

sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, 'source/')))
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, 'source/apps')))
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, 'source/apps/ext')))
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, 'source/lib')))
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, 'source/lib/ext')))

ADMINS = [
     ('Alerts', 'alert@webriders.com.ua'),
]

MANAGERS = [
     ('Info', 'info@webriders.com.ua'),
]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'site@webriders.com.ua'
EMAIL_HOST_PASSWORD = '93W374'
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[TechBlog] '

# New DB-settings style (Django 1.2+)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath('db/database.sqlite')
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

#LANGUAGES = (
#             ('ru', u'Русский'),
#             ('en', u'English'),
#             ('uk', u'Український'),
#             )
#

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'
ADMIN_MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'adminmedia') 

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c^7$)t^ka7oe+z6nfw)#$10auo=_$5oqv%6@nhhzm%k5s$1mxr'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(PROJECT_ROOT, "source/templates",),
)

# Default list of context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf'
)

INSTALLED_APPS = (
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',

    # External apps
    'south',
    'registration',
    'markitup',
    'haystack',
    'taggit',
    'threadedcomments',

    # Internal apps
    'techblog',
)

INTERNAL_IPS = ('127.0.0.1', 'localhost', 'django.local')

COMMENTS_APP = 'threadedcomments'
