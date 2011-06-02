from django.views.generic.list_detail import object_list, object_detail
from django.views.generic import ListView
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from datetime import datetime

from techblog.forms import ArticleForm
from techblog.models import Article, UserProfile


class ArticleList(ListView):
    context_object_name = 'article_list'
    template_name = 'articles/article_list.html'

    def get_queryset(self):
        filters = {}
        filters['is_public'] = True

        author = self.request.GET.get("author", None)
        if author:
            filters['author'] = author

        tags = self.request.GET.get("tags", None)
        if tags:
            filters['tags__name__in'] = tags.split(',')

        return Article.objects.filter(**filters).distinct().order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['page'] = 'articles_page'

        author_id = self.request.GET.get("author", None)
        if author_id:
            context['author'] = UserProfile.objects.get(id = author_id).user

        user = self.request.user
        if user.is_authenticated() and str(user.id) == author_id:
            context['edit_allowed'] = True

        context['tags'] = self.request.GET.get("tags", '')
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
                return redirect('view_article', article.id)
        else:
            form = ArticleForm(instance=article) # An unbound form
        params['form'] = form
    return direct_to_template(request, 'articles/add_or_edit_article.html', params)


def view_article(request, article_id=None, params={}, *args, **kwargs):
    params['page'] = 'view_article'
    articles = Article.objects.filter(is_public=True).order_by('-date')
    return object_detail(request, articles, article_id, template_name='articles/view_article.html', extra_context=params)
