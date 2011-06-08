from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from techblog.models import Article
from techblog.service.articles import TagFilter

class TestArticleService(TestCase):
    fixtures = ['test_data.json',]

    def setUp(self):
        pass

    def test_tag_filter_single_value(self):
#        types = ContentType.objects.all()
#        for t in types:
#            print str(t.id) + " :" + str(t)
#
#
        tag_filter = TagFilter(is_multivalue=True)
        tag_filter.value = ['south']
        query = Article.objects.all()
        query = tag_filter.filter(query)
        self.assertEqual(len(query), 2)

        context = tag_filter.get_context_data(query)
        self.assertTrue(context.has_key('tag_cloud'))
        self.assertEqual(len(context['tag_cloud']), 7)

        for tag in context['tag_cloud']:
            if tag.slug == "south":
                self.assertEqual(tag.count, 2)
                self.assertTrue(tag.selected)
                self.assertFalse(hasattr(tag, 'disabled'))

        print str(context)
