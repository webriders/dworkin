# -*- coding: UTF-8 -*-

from copy import copy, deepcopy
from django.contrib.auth.models import User
from markdown import markdown
from docutils.core import publish_parts
from textile import textile
from taggit.models import Tag

from techblog.filter.filter import Filter, FilterItem
from techblog.logic.mail_service import MailService
from techblog.models import Article, Category, Language
from techblog.services.categories import CategoryService
from techblog.services.tags import TagService
from techblog.services.languages import LanguageService
from techblog.functions import html_parser
from techblog.constants import LATEST_FEED_COUNT


class OwnerFilter(FilterItem):
    name="own"

    def __init__(self, is_multivalue=False, always_use=False):
        super(OwnerFilter, self).__init__(is_multivalue, always_use=True)

    def filter(self, query):
        if self.value and self.user and self.user.is_authenticated:
            if self.value == "articles":
                query = query.filter(authors__in=[self.user.id], is_public=True)
            elif self.value == "drafts":
                query = query.filter(authors__in=[self.user.id], is_public=False)
        else:
            query = query.filter(is_public=True)

        return query

    def get_context_data(self, filtered_ids):
        context = {}
        if self.user and self.user.is_authenticated():
            articles = ArticleService.get_articles_by_author(self.user)
            drafts = ArticleService.get_drafts_by_author(self.user)

#            if filtered_ids:
#                articles = articles.filter(id__in = filtered_ids)
#                drafts = drafts.filter(id__in = filtered_ids)
            context["own_articles_count"] = articles.count()
            context["own_drafts_count"] = drafts.count()

            if self.value == "articles":
                context["own_articles"] = True
            if self.value == "drafts":
                context["own_drafts"] = True
        return context


class LangFilter(FilterItem):
    name="langs"

    def filter(self, query):
        if self.value == "all":
            pass
        else:
            query = query.filter(lang__slug__in = self.value)
        return query

    def get_context_data(self, filtered_ids):
        languages = LanguageService.get_languages_with_count()

        if self.value:
            for lang in languages:
                if lang.slug in self.value:
                    lang.selected = True

        context = {"languages": languages}
        return context


class CategoryFilter(FilterItem):
    name="category"

    def filter(self, query):
        return query.filter(category__slug=self.value)

    def get_context_data(self, filtered_ids):
        all_categories = list(CategoryService.get_categories_with_count())
        filtered_categories = list(CategoryService.get_categories_with_count(filtered_ids))
        filtered_categories = dict(zip([cat.id for cat in filtered_categories], filtered_categories))

        for category in all_categories:
            if category.slug == self.value:
                category.selected = True
                category.count = filtered_categories[category.id].count
            if category.id not in filtered_categories.keys():
                category.disabled = True
                category.count = 0
        context = {"categories": all_categories}
        return context


class AuthorFilter(FilterItem):
    name="author"

    def filter(self, query):
        return query.filter(author__id=self.value)

    def get_context_data(self, filtered_ids):
        author = None
        try:
            author = User.objects.get(id=self.value)
        except User.DoesNotExist, e:
            pass
        return {"selected_author":author}


class TagFilter(FilterItem):
    name="tags"

    def filter(self, query):
        for tag in self.value:
            query = query.filter(tags__slug__in=[tag])
        return query

    def get_context_data(self, filtered_ids):
        selected_tag_slugs = []
        if self.value:
            selected_tags = TagService.get_by_slugs(self.value)
            selected_tag_slugs = [tag.slug for tag in selected_tags]

        all_tags = TagService.get_tag_cloud()
        filtered_tags = list(TagService.get_filtered_tag_cloud(filtered_ids))
        filtered_tags = dict(zip([tag.id for tag in filtered_tags], filtered_tags))

        # mark selected
        for tag in all_tags:
            # tag is selected
            if selected_tag_slugs and (tag.slug in selected_tag_slugs):
                tag.selected = True

            if tag.id in filtered_tags.keys():
                tag.count = filtered_tags[tag.id].count
            else:
                tag.disabled = True
                tag.count = 0

        context = {"tag_cloud": all_tags}
        return context

class ArticleService(object):
    mail_service = MailService()

    def init_filters(self):
        self.filter = Filter()
        self.filter.add_item(OwnerFilter())
        self.filter.add_item(LangFilter(is_multivalue=True))
        self.filter.add_item(CategoryFilter())
        self.filter.add_item(TagFilter(is_multivalue=True))
        self.filter.add_item(AuthorFilter())

    def filter_articles(self, request):
        query = Article.objects.all()
        self.init_filters()
        query = self.filter.filter_query(request, query)
        return query

    def get_current_filters(self):
        params = self.filter.get_params()
        current_filters = []

        #-------------------------------------
        own = params.get('own')
        if own:
            if own == 'articles':
                own = u'Статьи'
            elif own == 'drafts':
                own = u'Черновики'

            current_filters.append({
                    'name': 'own',
                    'value': own,
                    'slug': None,
                })

        #-------------------------------------
        category_slug = params.get('category')
        if category_slug:

            category = Category.objects.filter(slug=category_slug)
            if category:
                current_filters.append({
                    'name': 'category',
                    'value': category[0].title,
                    'slug': category_slug,
                })

        #------------------------------------
        tags = params.get('tags')
        if tags:
            for tag_slug in tags:

                tag = Tag.objects.filter(slug=tag_slug)
                if tag:
                    current_filters.append({
                        'name': 'tag',
                        'value': tag[0].name,
                        'slug': tag_slug
                    })
            del params['tags']

        return current_filters


    def get_control_panel_context(self, filtered_items):
        context = self.filter.get_context_data(filtered_items)
        context["filter"] = filter
        context['current_filters'] = self.get_current_filters()
        return context

    @staticmethod
    def get_feed_articles():
        return Article.get_published()[:LATEST_FEED_COUNT]

    @staticmethod
    def get_articles_by_author(user, ids=None):
        query = Article.objects.filter(authors__in=[user], is_public=True)
        if ids:
            query = query.filter(id__in=ids)
        return query

    @staticmethod
    def get_drafts_by_author(user, ids=None):
        query = Article.objects.filter(authors__in=[user], is_public=False)
        if ids:
            query = query.filter(id__in=ids)
        return query

    @staticmethod
    def get_article_ids_by_category(category):
         return Article.objects.filter(category=category, is_public=True).only("id")

    def publish_article(self, article, user=None):
        article.is_public = True
        article.save()
        self.mail_service.send_mail_on_first_article_publish(article, user)

    def unpublish_article(self, article, user=None):
        article.is_public = False
        article.save()
        self.mail_service.send_mail_on_article_unpublish(article, user)

    @staticmethod
    def render_markup(markup, raw_data):
        data = raw_data

        if markup == Article.MARKUP_MARKDOWN:
            data = markdown(data)
        elif markup == Article.MARKUP_RST:
            data = publish_parts(source=data, writer_name="html4css1")["fragment"]
        elif markup == Article.MARKUP_TEXTILE:
            data = textile(data)
        data = html_parser(data)

        return data

    @classmethod
    def render_markups(cls, article):

        class RenderedArticle(object):
            def __init__(self, short, description):
                self.short = short
                self.description = description

        markup = article.markup
        short = cls.render_markup(markup, article.short_raw)
        description = cls.render_markup(markup, article.description_raw)

        return RenderedArticle(short, description)

    @classmethod
    def get_translation_data(cls, article, user):
        trans_article = {}

        trans_article['title'] = article.title
        trans_article['lang'] = article.lang
        trans_article['category'] = article.category
        trans_article['tags'] = ', '.join(tag.name for tag in article.tags.all())
        trans_article['markup'] = article.markup
        trans_article['short_raw'] = article.short_raw
        trans_article['description_raw'] = article.description_raw

        trans_article['parent'] = article
        if article.is_original():
            trans_article['original'] = article
        else:
            trans_article['original'] = article.original

        return trans_article
