from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.views.generic.base import TemplateView
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic import ListView, DetailView, RedirectView, CreateView
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime

from techblog.forms import ArticleForm, TranslateArticleForm
from techblog.models import Article, UserProfile, Category, Language
from techblog.services.articles import ArticleService
from techblog.logic.mail_service import MailService
from techblog.constants import ARTICLES_LIMIT


class ArticlesControlPanel(object):
    article_service = ArticleService()

    def init_articles(self):
        self.articles = self.article_service.filter_articles(self.request).order_by('-date')

    def get_control_panel_context(self):
        return self.article_service.get_control_panel_context(self.articles)


class ArticleList(TemplateView, ArticlesControlPanel):
    template_name = 'articles/article_list.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['page'] = 'articles_page'

        self.init_articles()
        context.update(self.get_control_panel_context())

        if context.has_key('own_articles'):
            context['own'] = 'articles'
        elif context.has_key('own_drafts'):
            context['own'] = 'drafts'

        paginator = Paginator(list(self.articles), ARTICLES_LIMIT)

        try:
            page_num = int(self.request.GET.get('page', '1'))
        except ValueError:
            page_num = 1
        try:
            current_page = paginator.page(page_num)
        except (EmptyPage, InvalidPage):
            current_page = paginator.page(paginator.num_pages)
        context["article_list"] = list(current_page.object_list)

        if current_page.has_next():
            preview_page = paginator.page(page_num + 1)
            context['next_page'] = page_num + 1
            context['preview_articles'] = list(preview_page.object_list)

        return context


class TranslateArticle(CreateView):
    template_name = 'articles/translate_article.html'
    form_class = TranslateArticleForm

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user

        if 'is_public' in self.request.POST:
            form.instance.is_public = True
        else:
            form.instance.is_public = False

        form.save()
        form.instance.authors.add(self.request.user)

        if form.instance.is_public:
            MailService().send_mail_on_first_article_publish(form.instance, self.request.user)

        return redirect( reverse('view_article', args=(form.instance.id,)) )

    def get_initial(self):
        initial = super(TranslateArticle, self).get_initial().copy()
        article_id = self.kwargs.get('article_id')

        article = get_object_or_404(Article, id=article_id)
        data = ArticleService.get_translation_data(article, self.request.user)

        initial.update(data)
        return initial

translate_article = TranslateArticle.as_view()


def add_or_edit_article(request, article_id=None, action=None):
    mail_service = MailService()

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
            except Article.DoesNotExist:
                pass

        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                # Process the data in form.cleaned_data
                article = form.save(commit=False)
                if 'is_public' in request.POST:
                    article.is_public = True
                    if not article.date:
                        article.date = datetime.now()
                else:
                    article.is_public = False
                article.author = request.user # Todo: remove this
                article.save()
                article.authors.add(request.user)
                
                tags = form.cleaned_data['tags']
                article.tags.clear()
                for tag in tags:
                   article.tags.add(tag)

                if article.is_public:
                    mail_service.send_mail_on_first_article_publish(article, request.user)
                return redirect('/articles/%s/' % article.id)
        else:
            form = ArticleForm(instance=article) # An unbound form
        params['form'] = form
    return direct_to_template(request, 'articles/add_or_edit_article.html', params)


class ArticleDetail(DetailView, ArticlesControlPanel):
    template_name = 'articles/view_article.html'

    def get_object(self, queryset=None):
        article = get_object_or_404(Article, id=(self.kwargs.get('article_id')))

        self.is_public = article.is_public
        if article.is_public or self.request.user in article.authors.all():
            return article
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        self.init_articles()
        context.update(self.get_control_panel_context())
        context['page'] = 'articles_page'
        context['sub_page'] = 'view_article'
        context['is_public'] = self.is_public
        if self.object:
            context['edit_allowed'] = self.object.author == self.request.user

        return context


class ArticlePublisher(RedirectView):
    permanent = False
    article_service = ArticleService()

    def get_redirect_url(self, **kwargs):
        article_id, action =  self.args
        article = get_object_or_404(Article, id=article_id)
        url = '/articles/%s/' % article_id
        if article.author == self.request.user:
            if action == 'publish':
                self.article_service.publish_article(article, self.request.user)
            elif action == 'unpublish':
                self.article_service.unpublish_article(article, self.request.user)
        return url
