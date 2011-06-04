#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from techblog.functions import html_parser, binary_date, formatted_date
from techblog.constants import GENDER_MALE, GENDER_FEMALE
from django.conf import settings


class Article(models.Model):
    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'Статьи'

    def __unicode__(self):
        return self.title

    author = models.ForeignKey(User, verbose_name=u'Автор', null=True)
    title = models.CharField(u'Заголовок статьи', max_length=1024)
    date = models.DateTimeField(u'Время публикации', default=datetime.now())
    is_public = models.BooleanField(u'Статья опубликована?', default=False)
    markup = models.CharField(u'Формат', max_length=16, default='html')
    short_raw = models.TextField(u'Начало')
    description_raw = models.TextField(u'Под катом', blank=True)

    short = models.TextField(u'Начало')
    description = models.TextField(u'Под катом', blank=True)
    tags = TaggableManager(blank=True)

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
    gender = models.CharField('Пол', max_length=16, choices=GENDERS, blank=True, null=True)
    birth_date = models.DateField(u'Дата рождения', blank=True, null=True)
    avatar = ImageField(u'Фото', blank=True, null=True, upload_to='users/')
    use_gravatar = models.BooleanField(u'Использовать Gravatar', default=False)

    def get_articles_count(self):
        query = Article.objects.filter(author=self).count()
        return query

    def gravatar(self): pass

def handle_user_creation_signal(sender, **kwargs):
    """
     Unfortunately, User's profile doesn't created automatically. Thus we need to handle User creation signal.
    """
    if kwargs.get('created', False):
        profile = UserProfile()
        profile.user = kwargs.get('instance')
        profile.save()
post_save.connect(handle_user_creation_signal, sender=User)
