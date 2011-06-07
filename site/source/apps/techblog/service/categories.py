from django.db.models.aggregates import Count
from techblog.models import Category

class CategoryService(object):

    @staticmethod
    def get_categories_with_count(ids=None):
        categories = Category.objects.all()
        categories = categories.annotate(count=Count('article__id')).filter(count__gt=0).order_by('-count')
        if ids:
            categories = categories.filter(article__id__in = ids)
        return categories
  