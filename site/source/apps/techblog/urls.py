from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from techblog import views
from techblog.feeds import ArticlesFeed

urlpatterns = patterns('techblog.views',
    (r'^(?:articles/)?$', views.ArticleList.as_view()),
    (r'^articles/add/$', 'add_or_edit_article'),
    url(r'^articles/(?P<article_id>\d+)/$', views.ArticleDetail.as_view(), name='view_article'),
    (r'^articles/(\d+)/edit/$', 'add_or_edit_article'),
    (r'^articles/(\d+)/(publish|unpublish)/$', views.ArticlePublisher.as_view()),

    (r'^markitup/preview/(\w+)/$', views.MarkitupPreviewer.as_view()),

    (r'^users/$', views.UserProfilesList.as_view()),
    (r'^users/(?P<user_name>\w+)/$', views.UserProfileDetail.as_view()),
    (r'^profile/$', views.UserProfileDetail.as_view()),
    (r'^profile/edit/$', views.UserProfileEdit.as_view()),
    (r'^users/(?P<user_name>\w+)/marked/$', 'marked_by_user'),

    (r'^tags/$', views.TagsList.as_view()),

    (r'^api/parse_html/$', 'parse_html'),

    url(r'^rss/$', ArticlesFeed(), name='rss'),

)
