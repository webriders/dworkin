# -*- coding: UTF-8 -*-

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from techblog.services.articles import ArticleService
from django.utils.feedgenerator import Rss201rev2Feed

class TextXmlFeedType(Rss201rev2Feed):
    mime_type = 'text/xml'

class ArticlesFeed(Feed):

    title = u"Блог Progressors.org.ua"
    link = "/rss/"
    description = u"Новые статьи на Progressors.org.ua"
    feed_type = TextXmlFeedType

    def items(self):
        blog_articles = ArticleService.get_feed_articles()
        return blog_articles

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return reverse('view_article', kwargs={'article_id':item.id})

    def item_description(self, item):
        return item.short

    def item_pubdate(self, item):
        return item.date
