from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from techblog.models import Article
from techblog.services.articles import ArticleService, TagFilter, OwnerFilter, CategoryFilter


class Request(object):
    def __init__(self):
        self.GET = {}
        self.user = AnonymousUser()


class TestArticleService(TestCase):
    fixtures = ['test_data.json',]

    def test_article_filters_for_anonymous(self):

        article_service = ArticleService()

        request = Request()
        query = article_service.filter_articles(request)
        self.assertEqual(len(query), 39)

        request = Request()
        request.GET['own'] = 'articles'
        query = article_service.filter_articles(request)
        self.assertEqual(len(query),39)

        request = Request()
        request.GET['own'] = 'drafts'
        query = article_service.filter_articles(request)
        self.assertEqual(len(query),39)


    def test_article_filters_for_authorized(self):

        article_service = ArticleService()

        #-------------------------------------------------------
        user_lexa = User.objects.get(username='lexa')

        request = Request()
        request.user = user_lexa
        query = article_service.filter_articles(request)
        self.assertEqual(len(query), 39)

        request = Request()
        request.user = user_lexa
        request.GET['own'] = 'articles'
        query = article_service.filter_articles(request)
        self.assertEqual(len(query), 6)

        request = Request()
        request.user = user_lexa
        request.GET['own'] = 'drafts'
        query = article_service.filter_articles(request)
        self.assertEqual(len(query), 1)

        #-------------------------------------------------------
        user_kottenator = User.objects.get(username='kottenator')

        request = Request()
        request.user = user_kottenator
        query = article_service.filter_articles(request)
        self.assertEqual(len(query), 39)

        request = Request()
        request.user = user_kottenator
        request.GET['own'] = 'articles'
        query = article_service.filter_articles(request)
        self.assertEqual(len(query), 18)

        request = Request()
        request.user = user_kottenator
        request.GET['own'] = 'drafts'
        query = article_service.filter_articles(request)
        self.assertEqual(len(query), 0)


class TestTagFilter(TestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
        from django.contrib.contenttypes.models import ContentType
        from taggit.models import TaggedItem

        article_content_type = ContentType.objects.get(model='article')
        TaggedItem.objects.update(content_type=article_content_type)

    def test_tag_filter_single_value(self):
        tag_filter = TagFilter(is_multivalue=True)
        tag_filter.value = ['south']
        query = Article.get_published()
        query = tag_filter.filter(query)
        self.assertEqual(len(query), 2)

        context = tag_filter.get_context_data([item.id for item in query])
        self.assertTrue(context.has_key('tag_cloud'))
        self.assertEqual(len(context['tag_cloud']), 7)

        for tag in context['tag_cloud']:
            if tag.slug == "south":
                self.assertEqual(tag.count, 2)
                self.assertTrue(tag.selected)
                self.assertFalse(hasattr(tag, 'disabled'))

    def test_tag_filter_decreased_count(self):
        tag_filter = TagFilter(is_multivalue=True)
        tag_filter.value = ['refactoring']
        query = Article.get_published()
        query = tag_filter.filter(query)
        context = tag_filter.get_context_data([item.id for item in query])

        for tag in context['tag_cloud']:
            if tag.slug == "south":
                self.assertEqual(tag.count, 1)


class TestOwnFilter(TestCase):
    fixtures = ['test_data.json',]

    def test_own_filter_anonymous(self):
        filter = OwnerFilter()
        filter.value = 'articles'
        query = Article.get_published()
        query = filter.filter(query)
        self.assertEqual(len(query), 39)

        context = filter.get_context_data([item.id for item in query])
        self.assertFalse(context.has_key('own_articles'))
        self.assertFalse(context.has_key('own_articles_count'))
        self.assertFalse(context.has_key('own_drafts'))
        self.assertFalse(context.has_key('own_drafts_count'))


    def test_own_filter_articles(self):
        filter = OwnerFilter()
        filter.value = 'articles'
        filter.user = User.objects.get(username="lexa")
        query = Article.get_published()
        query = filter.filter(query)
        self.assertEqual(len(query), 6)

        context = filter.get_context_data([item.id for item in query])
        self.assertTrue(context.has_key('own_articles'))
        self.assertEqual(context['own_articles_count'], 6)
        self.assertEqual(context['own_drafts_count'], 1)

    def test_own_filter_drafts(self):
        filter = OwnerFilter()
        filter.value = 'drafts'
        filter.user = User.objects.get(username="lexa")
        query = Article.objects.filter()
        query = filter.filter(query)
        self.assertEqual(len(query), 1)   #

        context = filter.get_context_data([item.id for item in query])
        self.assertTrue(context.has_key('own_drafts'))
        self.assertEqual(context['own_articles_count'], 6)
        self.assertEqual(context['own_drafts_count'], 1)


class TestCategoryFilter(TestCase):
    fixtures = ['test_data.json',]

    def test_filter(self):
        filter = CategoryFilter()
        filter.value = "django"
        query = Article.get_published()
        query = filter.filter(query)
        self.assertEqual(len(query), 2)


    def test_get_context_data(self):
        filter = CategoryFilter()
        filter.value = "django"

        query = Article.objects.filter(is_public=True, category__slug='django')
        context = filter.get_context_data([item.id for item in query])
        self.assertEqual(len(context['categories']), 3)
        self.assertEqual(context['categories'][0].selected, True)
        self.assertEqual(context['categories'][0].count, 2)
        self.assertEqual(context['categories'][1].count, 0)
        self.assertEqual(context['categories'][2].count, 0)

