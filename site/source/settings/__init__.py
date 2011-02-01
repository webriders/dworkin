"""
Django project settings.
Separated into Python-package and divided into files
"""
import platform
import sys

# Applications settings
from apps_settings import *

# Load main settings.
from main_settings import *

DEPLOYMENT_SERVERS = ('webriders',)
DEPLOYMENT = platform.node() in DEPLOYMENT_SERVERS

if DEPLOYMENT:
    from deployment_settings import *
else:
    from local_settings import *

pass
