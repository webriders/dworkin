from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

urlpatterns = patterns('techblog.views',
    (r'^(?:articles/)?$', 'article_list'),
    (r'^articles/add/$', 'add_or_edit_article'),
    url(r'^articles/(\d+)/$', 'view_article', name='view_article'),
    (r'^articles/(\d+)/edit/$', 'add_or_edit_article'),

    (r'^users/$', 'user_list'),
    (r'^users/(?P<user_name>\w+)/$', 'user_profile'),
    (r'^users/(?P<user_name>\w+)/creative/$', 'user_creative'),
    (r'^users/(?P<user_name>\w+)/marked/$', 'marked_by_user'),

    (r'^tags/$', 'tag_cloud'),

    (r'^api/parse_html/$', 'parse_html'),
)
