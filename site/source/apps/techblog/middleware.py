from django.conf import settings
import django.core.exceptions
from django.http import HttpResponseRedirect
from django.utils import translation
# TODO importing undocumented function
from django.utils.translation.trans_real import parse_accept_lang_header
from localeurl import settings as localeurl_settings
from localeurl import utils
from models import *
from lib.utils.log import logger

# Make sure the default language is in the list of supported languages
assert utils.supported_language(settings.LANGUAGE_CODE) is not None, \
        "Please ensure that settings.LANGUAGE_CODE is in settings.LANGUAGES."

class LocaleURLMiddleware(object):
    """
    Used to process "/" requests, like http://www.website.com and set the correct content language.

    1. Check if path is empty.
    2. Check if resident is present in cookie. If so - use language from resident.
    3. If resident is not present - use accept language from browser settings.
    """
    def process_request(self, request):
        logger.debug("PATH:" + request.path_info + " Independent:" + str(utils.is_locale_independent(request.path_info))) 
        locale, path = utils.strip_path(request.path_info)
        logger.debug("locale:" + locale + " path:" + path)
        if not locale and not utils.is_locale_independent(request.path_info):
            locale = self.get_accept_language(request)

        locale_path = utils.locale_path(path, locale)
        logger.debug("locale path:" + locale_path)
        if locale_path != request.path_info:
            if request.META.get("QUERY_STRING", ""):
                locale_path = "%s?%s" % (locale_path,
                        request.META['QUERY_STRING'])
            logger.debug("redirecting to locale path:" + locale_path)
            return HttpResponseRedirect(locale_path)
        request.path_info = path
        if not locale:
            try:
                locale = request.LANGUAGE_CODE
            except AttributeError:
                locale = settings.LANGUAGE_CODE
        translation.activate(locale)
        request.LANGUAGE_CODE = translation.get_language()

    def get_accept_language(self, request):
        accept_locale = None
        accept_langs = filter(lambda x: x, [utils.supported_language(lang[0])
                                    for lang in
                                    parse_accept_lang_header(
                        request.META.get('HTTP_ACCEPT_LANGUAGE', ''))])
        if accept_langs:
            accept_locale = accept_langs[0]
        logger.debug("locale from ACCEPT_LANGUAGE:" + accept_locale)
        return accept_locale

    def process_response(self, request, response):
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response

