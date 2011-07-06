#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.db.models.fields.files import ImageField
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from techblog.functions import html_parser, binary_date, formatted_date
from techblog.constants import GENDER_MALE, GENDER_FEMALE
from django.conf import settings

class Category(models.Model):
    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'
        ordering = ('title',)

    title = models.CharField(max_length=64, verbose_name=u'Заголовок')
    slug = models.SlugField(max_length=64, verbose_name=u'Текстовая ссылка на статью в броузере', help_text=u'только анг.буквы, пример time_management_for_the_masses', default="")

    def __unicode__(self):
        return self.title

#    def show_article_count(self):
#        return create_linked_models_html(self.blogarticle_set.all(), "blog", 'blogarticle')
#    show_article_count.short_description = u'Число статей по категории'
#    show_article_count.allow_tags = True

    @staticmethod
    def get_categories_with_count():
        categories = Category.objects.all()
        categories = categories.annotate(count=Count('article__id')).filter(count__gt=0).order_by('-count')
        return categories

class Article(models.Model):
    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'Статьи'

    def __unicode__(self):
        return self.title

    author = models.ForeignKey(User, verbose_name=u'Автор', null=True)
    authors = models.ManyToManyField(User, verbose_name=u'Авторы', null=True, related_name='authors')
    title = models.CharField(u'Заголовок статьи', max_length=1024)
    date = models.DateTimeField(u'Время публикации', default=datetime.now())
    is_public = models.BooleanField(u'Статья опубликована?', default=False)
    markup = models.CharField(u'Формат', max_length=16, default='html')
    short_raw = models.TextField(u'Начало')
    description_raw = models.TextField(u'Под катом', blank=True)

    short = models.TextField(u'Начало')
    description = models.TextField(u'Под катом', blank=True)
    tags = TaggableManager(blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)


    def save(self, *args, **kwargs):
        self.short = html_parser(self.short_raw)
        self.description = html_parser(self.description_raw)
        super(Article, self).save(*args, **kwargs) # Call the "real" save() method.

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
        verbose_name = u'профиль'
        verbose_name_plural = u'Профили пользователей'

    def __unicode__(self):
        return u'Профиль пользователя %s' % self.user.username

    user = models.ForeignKey(User, unique=True)
    GENDERS = (
        (GENDER_MALE, u'Мужской'),
        (GENDER_FEMALE, u'Женский'),
    )
    gender = models.CharField(u'Пол', max_length=16, choices=GENDERS, blank=True, null=True)
    birth_date = models.DateField(u'Дата рождения', blank=True, null=True)
    avatar = ImageField(u'Фото', blank=True, null=True, upload_to='users/')
    use_gravatar = models.BooleanField(u'Использовать Gravatar', default=False)
    about_me = models.TextField(u'Про себя', max_length=4096, blank=True, null=True)
    visible = models.BooleanField(u'Показывать на странице с авторами', default=True)
    
    def get_articles_count(self):
        query = Article.objects.filter( authors__in=[self] ).count()
        return query

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
