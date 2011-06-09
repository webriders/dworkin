from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime

from techblog.forms import ArticleForm
from techblog.models import Article, UserProfile, Category
from techblog.service.articles import ArticleService
from techblog.service.tags import TagService
from techblog.constants import ARTICLES_LIMIT


class ArticleList(ListView):
    context_object_name = 'article_list'
    template_name = 'articles/article_list.html'

    def get_queryset(self):
        self.article_service = ArticleService()
        articles = self.article_service.filter_articles(self.request).order_by('-date')

#        filters = {}
#        filters['is_public'] = True
#
#        author = self.request.GET.get("author", None)
#        if author:
#            filters['author'] = author
#
#        tags = self.request.GET.get("tags", None)
#        if tags:
#            filters['tags__name__in'] = tags.split(',')
#
#        articles =  Article.objects.filter(**filters).distinct().order_by('-date')
        if articles:

            self.paginator = Paginator(articles, ARTICLES_LIMIT)

            page_num = self.request.GET.get('page', 1)
            try:
                page = self.paginator.page(page_num)
            except PageNotAnInteger:
                page = self.paginator.page(1)
            except EmptyPage:
                page = self.paginator.page(self.paginator.num_pages)

            return page
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['page'] = 'articles_page'

        if self.object_list:
            context.update(self.article_service.get_control_panel_context(self.object_list.object_list))

        if context.has_key('own_articles'):
            context['own'] = 'articles'
        elif context.has_key('own_drafts'):
            context['own'] = 'drafts'


#        context["categories"] = Category.get_categories_with_count()
#        context["tag_cloud"] = TagService.get_tag_cloud()

        author_id = self.request.GET.get("author", None)
        if author_id:
            context['author'] = UserProfile.objects.get(id = author_id).user

        user = self.request.user
        if user.is_authenticated() and str(user.id) == author_id:
            context['edit_allowed'] = True

#        context['tags'] = self.request.GET.get("tags", '')

        if self.object_list:
            try:
                page_num = int(self.request.GET.get("page", ''))
            except ValueError:
                page_num = 1

            context['page_num'] = page_num
            current_page = self.paginator.page(page_num)

            if current_page.has_next():
                preview_page = self.paginator.page(page_num + 1)
                context['next_page'] = page_num + 1
                context['preview_articles'] = list(preview_page.object_list)

        return context

def add_or_edit_article(request, article_id=None):
    params = {}

    if request.user.is_authenticated():
        params['page'] = 'add_article'
        params['edit_allowed'] = True

        article = None
        if article_id:
            try:
                article = Article.objects.get(id=article_id)
                if article.author == request.user:
                    params['page'] = 'edit_article'
                else:
                    params['edit_allowed'] = False
            except:
                pass

        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                # Process the data in form.cleaned_data
                article = form.save(commit=False)
                article.author = request.user
                if 'is_public' in request.POST:
                    article.is_public = True
                    if not article.date:
                        article.date = datetime.now()
                else:
                    article.is_public = False
                article.save()
                
                tags = form.cleaned_data['tags']
                for tag in tags:
                   article.tags.add(tag)

                if article.is_public:
                    return redirect('/?own=articles')
                else:
                    return redirect('/?own=drafts')
        else:
            form = ArticleForm(instance=article) # An unbound form
        params['form'] = form
    return direct_to_template(request, 'articles/add_or_edit_article.html', params)


class ArticleDetail(DetailView):
    template_name = 'articles/view_article.html'

    def get_object(self, queryset=None):
        article = get_object_or_404(Article, id=(self.kwargs.get('article_id')))

        self.is_public = article.is_public
        if article.is_public:
            return article
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)

        context['page'] = 'articles_page'
        context['sub_page'] = 'view_article'
        context['is_public'] = self.is_public
        if self.object:
            context['edit_allowed'] = self.object.author == self.request.user

        return context


class ArticlePublisher(RedirectView):
    def get_redirect_url(self, **kwargs):
        article_id, action =  self.args
        article = get_object_or_404(Article, id=article_id)
        url = '/'
        if article.author == self.request.user:
            if action == 'publish':
                article.is_public = True
                url = '/?own=articles'
            elif action == 'unpublish':
                article.is_public = False
                url = '/?own=drafts'
            article.save()
        return url