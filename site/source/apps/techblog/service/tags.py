from django.db.models.aggregates import Count
from taggit.models import TaggedItem, Tag


class TagService(object):

    @staticmethod
    def get_tag_cloud():
        tags = Tag.objects.annotate(count=Count("taggit_taggeditem_items__id")).filter(count__gt=0).order_by('name')
        return tags

    @staticmethod
    def get_filtered_tag_cloud(article_ids):
        tags = Tag.objects.filter(taggit_taggeditem_items__object_id__in=article_ids)
        tags = tags.annotate(count=Count("taggit_taggeditem_items__id")).filter(count__gt=0).order_by('name')
        print tags.query
        return tags


    @staticmethod
    def get_by_slugs(slugs=None):
        tags = Tag.objects.filter(slug__in=slugs)
        return tags


