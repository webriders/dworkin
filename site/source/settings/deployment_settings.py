# -*- coding: UTF-8 -*-

"""
Part of settings.py that contains Deployment settings. Not standalone!
"""


DEBUG = False
TEMPLATE_DEBUG = DEBUG

#-- Email
"""
EMAIL_HOST = "pleso.net"
EMAIL_PORT = "25"
EMAIL_HOST_USER = "bot@inmind.org"
EMAIL_HOST_PASSWORD = ""
EMAIL_SUBJECT_PREFIX = "website (local) - "
"""

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
