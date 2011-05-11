from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ## External applications mappings
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
	## Internal applications mappings
    (r'', include('techblog.urls')),
)
     
# Adding debug-mappings
if settings.DEBUG:
    from django.conf.urls.static import static
    # Debug media and static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
