from django.db.models.aggregates import Count
from taggit.models import TaggedItem, Tag


class TagService(object):

    @staticmethod
    def get_tag_cloud():
        tags = Tag.objects.annotate(count=Count("taggit_taggeditem_items__id")).filter(count__gt=0)
        print str(tags)
        return tags
