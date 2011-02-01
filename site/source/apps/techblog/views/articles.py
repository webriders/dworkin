from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from datetime import datetime


from techblog.forms import ArticleForm
from techblog import models
from techblog.models import Article


def article_list(request):
    params = dict(page='article_list')
    articles = models.Article.objects.filter(is_public=True).order_by('-date')
    return object_list(request, articles, template_name='articles/article_list.html', extra_context=params)


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
    articles = models.Article.objects.filter(is_public=True).order_by('-date')
    return object_detail(request, articles, article_id, template_name='articles/view_article.html', extra_context=params)
