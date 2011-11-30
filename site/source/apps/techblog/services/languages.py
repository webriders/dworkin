from django.db.models.aggregates import Count
from techblog.models import Language

class LanguageService(object):

    @classmethod
    def get_languages_with_count(cls):
        return Language.objects.annotate(count = Count('article')).filter(count__gt=0)