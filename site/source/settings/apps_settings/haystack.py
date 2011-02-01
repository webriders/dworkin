from .. import main_settings
import os

HAYSTACK_SITECONF = 'conf.haystack.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(main_settings.PROJECT_ROOT, 'search_index')
