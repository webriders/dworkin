from django.db.models.aggregates import Count
from taggit.models import TaggedItem, Tag


class TagService(object):

    @staticmethod
    def get_tag_cloud(ids=None):
        tags = Tag.objects.annotate(count=Count("taggit_taggeditem_items__id")).filter(count__gt=0)
        if ids:
            tags = tags.filter(taggit_taggeditem_items__id__in=ids)
        return tags

    @staticmethod
    def get_by_slugs(slugs=None):
        tags = Tag.objects.filter(slug__in=slugs)
        return tags


