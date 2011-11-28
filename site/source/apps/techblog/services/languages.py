from django.db.models.aggregates import Count
from techblog.models import Language

class LanguageService(object):

    @classmethod
    def get_languages_with_count(cls, ids=None):
        languages = cls.get_non_empty()
#        if ids:
#            languages = languages.filter(article__id__in = ids)
        languages = languages.annotate(count=Count('article__id')).filter(count__gt=0).order_by('-count')
        return languages

    @classmethod
    def get_non_empty(cls):
        return Language.objects.all().annotate(article_count = Count('article')).filter(article_count__gt=0)