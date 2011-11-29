#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.db.models.fields.files import ImageField
from django.db.models.signals import post_save
from django.db.models import Q
from taggit.managers import TaggableManager
from techblog.functions import html_parser, binary_date, formatted_date
from techblog.constants import GENDER_MALE, GENDER_FEMALE
from django.conf import settings


class Language(models.Model):
    class Meta:
        verbose_name = u'Language'
        verbose_name_plural = u'Languages'
        ordering = ('title',)

    title = models.CharField(max_length=25, verbose_name=u'Title')
    slug = models.SlugField(max_length=64, default="", unique=True, db_index=True, verbose_name=u'Slug')

    def __unicode__(self):
        return self.title


class Category(models.Model):
    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'
        ordering = ('title',)

    title = models.CharField(max_length=64, verbose_name=u'Title')
    slug = models.SlugField(max_length=64, verbose_name=u'Text link to the article in browser', help_text=u"only English letters, sample 'time_management_for_the_masses'", default="")

    def __unicode__(self):
        return self.title

    @staticmethod
    def get_categories_with_count():
        categories = Category.objects.all()
        categories = categories.annotate(count=Count('article__id')).filter(count__gt=0).order_by('-count')
        return categories


class Article(models.Model):
    class Meta:
        verbose_name = u'Article'
        verbose_name_plural = u'Articles'
        ordering = ('-date',)

    author = models.ForeignKey(User, verbose_name=u'Author', null=True, blank=True)
    authors = models.ManyToManyField(User, verbose_name=u'Authors', null=True, related_name='authors')
    title = models.CharField(u'Title', max_length=1024)
    date = models.DateTimeField(u'Publication date', default=datetime.now())
    is_public = models.BooleanField(u'Is published?', default=False)
    notified_on_first_publish = models.BooleanField(default=False, editable=False)

    lang = models.ForeignKey(Language, verbose_name=u'Language')
    parent = models.ForeignKey('self',  related_name='parent_article', blank=True, null=True, verbose_name=u'Parent', help_text='The article, which directly is translated.')
    original = models.ForeignKey('self', related_name='original_article', blank=True, null=True, verbose_name=u'Original', help_text='The original article.')

    MARKUP_HTML = u'html'
    MARKUP_MARKDOWN = u'markdown'
    MARKUP_RST = u'rst'
    MARKUP_TEXTILE = u'textile'
    MARKUP_TYPE = (
        (MARKUP_HTML, u'HTML'),
        (MARKUP_MARKDOWN, u'Markdown'),
        (MARKUP_RST, u'ReStructuredText'),
        (MARKUP_TEXTILE, u'Textile'),
    )
    markup = models.CharField(u'Format', max_length=16, default=MARKUP_HTML, choices=MARKUP_TYPE)
    short_raw = models.TextField(u'Short')
    description_raw = models.TextField(u'Undercut', blank=True)

    short = models.TextField(u'Short (result)')
    description = models.TextField(u'Undercut (result)', blank=True)
    tags = TaggableManager(blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)

    def __unicode__(self):
        return self.title

    @classmethod
    def get_published(cls):
        return cls.objects.filter(is_public=True)

    def get_translations(self):
        query = self.get_published()
        if self.is_original():
            query = query.filter(original=self)
        else:
            query = query.filter(Q(original=self.original) | Q(id=self.original.id), ~Q(id=self.id))
        query = query.select_related('author', 'lang')
        return query

    def save(self, *args, **kwargs):

        from techblog.services.articles import ArticleService
        rendered_article = ArticleService.render_markups(self)

        self.short = rendered_article.short
        self.description = rendered_article.description

        super(Article, self).save(*args, **kwargs) # Call the "real" save() method.

    def is_original(self):
        return self.original is None

    def binary_date(self):
        return binary_date(self.date)

    def formatted_date(self):
        return formatted_date(self.date)

    def get_absolute_url(self):
        return reverse('view_article', args=(self.id,))


class UserProfile(models.Model):
    """
     After profile is created you may access it from User instance: userobj.get_profile()
    """
    class Meta:
        verbose_name = u'User profile'
        verbose_name_plural = u'User profiles'

    def __unicode__(self):
        return u"Profile of user: '%s'" % self.user.username

    user = models.ForeignKey(User, unique=True)
    GENDERS = (
        (GENDER_MALE, u'Male'),
        (GENDER_FEMALE, u'Female'),
    )
    gender = models.CharField(u'Gender', max_length=16, choices=GENDERS, blank=True, null=True)
    birth_date = models.DateField(u'Birthday', blank=True, null=True)
    avatar = ImageField(u'Foto', blank=True, null=True, upload_to='users/')
    use_gravatar = models.BooleanField(u'Use Gravatar', default=False)
    about_me = models.TextField(u'About me', max_length=4096, blank=True, null=True)
    
    def get_articles_count(self):
        count = Article.objects.filter( authors__in=[self.user], is_public=True).count()
        return count

    def gravatar(self): pass

def handle_user_creation_signal(sender, instance, **kwargs):
    """
     Unfortunately, User's profile doesn't created automatically. Thus we need to handle User creation signal.
    """
    try:
        profile = instance.get_profile()
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=instance)
        profile.save()
post_save.connect(handle_user_creation_signal, sender=User)
