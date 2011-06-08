from techblog.filter.filter import Filter, FilterItem
from techblog.models import Article
from techblog.service.categories import CategoryService
from techblog.service.tags import TagService

class OwnerFilter(FilterItem):
    name="own"
    def filter(self, query):
        if self.user:
            if self.value == "articles":
                query = query.filter(author__id=self.user.id)
            if self.value == "drafts" :
                query = query.filter(author__id=self.user.id, is_public=False)
        return query

    def get_context_data(self, filtered_items):
        context = {}
        if self.value == "articles":
            context["own_articles"] = True
        if self.value == "drafts":
            context["own_drafts"] = True
        return context

class CategoryFilter(FilterItem):
    name="category"

    def filter(self, query):
        return query.filter(category__slug=self.value)

    def get_context_data(self, filtered_items):
        ids = []
        for item in filtered_items:
            ids.append(item.id)
        all_categories = list(CategoryService.get_categories_with_count())
        filtered_categories = list(CategoryService.get_categories_with_count(ids))
        filtered_ids = []
        for cat in filtered_categories:
            filtered_ids.append(cat.id)

        for category in all_categories:
            if category.slug == self.value:
                category.selected = True
            if category.id not in filtered_ids:
                category.disabled = True
        context = {"categories": all_categories}
        return context


class TagFilter(FilterItem):
    name="tags"

    def filter(self, query):
        return query.filter(tags__slug__in=self.value)

    def get_context_data(self, filtered_items):
        ids = []
        for item in filtered_items:
            ids.append(item.id)

        selected_tag_slugs = []
        if self.value:
            selected_tags = TagService.get_by_slugs(self.value)
            selected_tag_slugs = [tag.slug ]
            for t in selected_tags:
                selected_tag_slugs.append(t.slug)

        all_tags = TagService.get_tag_cloud()
        filtered_tags = TagService.get_filtered_tag_cloud(ids)
        filtered_ids = []
        for tag in filtered_tags:
            filtered_ids.append(tag.id)

        # mark selected
        for tag in all_tags:
            # tag is selected
            if selected_tag_slugs and (tag.slug in selected_tag_slugs):
                tag.selected = True
            # tag is disabled
            if tag.id not in filtered_ids:
                tag.disabled = True

        context = {"tag_cloud": all_tags}
        return context

class ArticleService(object):

    def __init__(self):
        self.filter = Filter()
        self.filter.add_item(OwnerFilter())
        self.filter.add_item(CategoryFilter())
        self.filter.add_item(TagFilter(is_multivalue=True))

    def filter_articles(self, request):
        query = Article.objects.all()
        if request.GET.get("own") != "drafts":
            query = query.filter(is_public=True)
        query = self.filter.filter_query(request, query)
        return query

    def get_control_panel_context(self, filtered_items):
        context = self.filter.get_context_data(filtered_items)
        context["filter"] = filter
        return context
