from django.contrib.auth.models import User
from techblog.filter.filter import Filter, FilterItem
from techblog.logic.mail_service import MailService
from techblog.models import Article
from techblog.services.categories import CategoryService
from techblog.services.tags import TagService

class OwnerFilter(FilterItem):
    name="own"
    def filter(self, query):
        if self.user and self.user.is_authenticated():
            if self.value == "articles":
                query = query.filter(authors__in=[self.user.id])
            if self.value == "drafts" :
                query = query.filter(authors__in=[self.user.id], is_public=False)
        return query

    def get_context_data(self, filtered_ids):
        context = {}
        if self.user and self.user.is_authenticated():
            context["own_articles_count"] = ArticleService.get_articles_by_author(self.user, filtered_ids).count()
            context["own_drafts_count"] = ArticleService.get_drafts_by_author(self.user, filtered_ids).count()
            if self.value == "articles":
                context["own_articles"] = True
            if self.value == "drafts":
                context["own_drafts"] = True
        return context

class CategoryFilter(FilterItem):
    name="category"

    def filter(self, query):
        return query.filter(category__slug=self.value)

    def get_context_data(self, filtered_ids):
        all_categories = list(CategoryService.get_categories_with_count())
        filtered_categories = list(CategoryService.get_categories_with_count(filtered_ids))
        filtered_categories = dict(zip([cat.id for cat in filtered_categories], filtered_categories))

        for category in all_categories:
            if category.slug == self.value:
                category.selected = True
                category.count = filtered_categories[category.id].count
            if category.id not in filtered_categories.keys():
                category.disabled = True
                category.count = 0
        context = {"categories": all_categories}
        return context

class AuthorFilter(FilterItem):
    name="author"

    def filter(self, query):
        print "AUTHOR: " + str(self.value)
        return query.filter(author__id=self.value)

    def get_context_data(self, filtered_ids):
        author = None
        try:
            author = User.objects.get(id=self.value)
        except User.DoesNotExist, e:
            pass
        return {"selected_author":author}


class TagFilter(FilterItem):
    name="tags"

    def filter(self, query):
        return query.filter(tags__slug__in=self.value)

    def get_context_data(self, filtered_ids):
        selected_tag_slugs = []
        if self.value:
            selected_tags = TagService.get_by_slugs(self.value)
            selected_tag_slugs = [tag.slug for tag in selected_tags]

        all_tags = TagService.get_tag_cloud()
        filtered_tags = list(TagService.get_filtered_tag_cloud(filtered_ids))
        filtered_tags = dict(zip([tag.id for tag in filtered_tags], filtered_tags))

        # mark selected
        for tag in all_tags:
            # tag is selected
            if selected_tag_slugs and (tag.slug in selected_tag_slugs):
                tag.selected = True

            if tag.id in filtered_tags.keys():
                tag.count = filtered_tags[tag.id].count
            else:
                tag.disabled = True
                tag.count = 0

        context = {"tag_cloud": all_tags}
        return context

class ArticleService(object):
    mail_service = MailService()

    def __init__(self):
        self.filter = Filter(store_in_session=True)
        self.filter.add_item(OwnerFilter())
        self.filter.add_item(CategoryFilter())
        self.filter.add_item(TagFilter(is_multivalue=True))
        self.filter.add_item(AuthorFilter())

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

    @staticmethod
    def get_articles_by_author(user, ids):
        return Article.objects.filter(author=user, is_public=True, id__in=ids)

    @staticmethod
    def get_drafts_by_author(user, ids):
        return Article.objects.filter(author=user, is_public=False, id__in=ids)

    @staticmethod
    def get_article_ids_by_category(category):
         return Article.objects.filter(category=category, is_public=True).only("id")

    def publish_article(self, article, user=None):
        article.is_public = True
        article.save()
        self.mail_service.send_mail_on_article_publish(article, user)

    def unpublish_article(self, article, user=None):
        article.is_public = False
        article.save()
        self.mail_service.send_mail_on_article_unpublish(article, user)
