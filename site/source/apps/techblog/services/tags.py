from django.db.models.aggregates import Count
from taggit.models import Tag


class TagService(object):

    @staticmethod
    def get_tag_cloud():
        tags = Tag.objects.annotate(count=Count("taggit_taggeditem_items__id")).filter(count__gt=0).order_by('name')
        return tags

    @staticmethod
    def get_filtered_tag_cloud(article_ids):
        tags = Tag.objects.filter(taggit_taggeditem_items__object_id__in=article_ids)
        tags = tags.annotate(count=Count("taggit_taggeditem_items__id")).filter(count__gt=0).order_by('name')
        return tags


    @staticmethod
    def get_by_slugs(slugs=None):
        tags = Tag.objects.filter(slug__in=slugs)
        return tags

    @staticmethod
    def get_category_tag_cloud():
        from techblog.services.articles import ArticleService
        from techblog.services.categories import CategoryService
        cats = CategoryService.get_categories_with_count()
        for category in cats:
            article_ids = ArticleService.get_article_ids_by_category(category)
            category.tags = list(TagService.get_filtered_tag_cloud([a.id for a in article_ids]))
            if not category.tags:
                category.empty = True
        return cats



