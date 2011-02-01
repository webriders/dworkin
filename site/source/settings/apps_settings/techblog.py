from .. import main_settings

## Overriding/adding MIDDLEWARE_CLASSES
#_wsm = 'website.middleware.LocaleURLMiddleware'
#if _wsm not in main_settings.MIDDLEWARE_CLASSES:
#    main_settings.MIDDLEWARE_CLASSES = (_wsm,) + main_settings.MIDDLEWARE_CLASSES
#
## Overriding/adding TEMPLATE_CONTEXT_PROCESSORS
#_wscx = 'website.context_processors.add_constants'
#if _wscx not in main_settings.TEMPLATE_CONTEXT_PROCESSORS:
#    main_settings.MIDDLEWARE_CLASSES += (_wscx,)

AUTH_PROFILE_MODULE = 'techblog.userprofile'

del main_settings