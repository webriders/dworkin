# -*- coding: UTF-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from markitup.widgets import MarkItUpWidget
from taggit.forms import TagWidget
from techblog.models import Article, UserProfile

class ArticleForm(forms.ModelForm):
    #short = forms.TextField()
    #description = forms.TextField()
    class Meta(object):
        model = Article
        fields = ('title', 'category', 'tags', 'markup', 'short_raw', 'description_raw', )
        widgets = {
            'short_raw': MarkItUpWidget(),
            'description_raw': MarkItUpWidget(),
            'tags' : TagWidget(),
        }


class UserForm(forms.ModelForm):
    oldpassword = forms.CharField( widget=forms.PasswordInput, label='Страрый пароль', required=False )
    password1 = forms.CharField( widget=forms.PasswordInput, label=u'Новый пароль', required=False )
    password2 = forms.CharField( widget=forms.PasswordInput, label=u'Пароля (верификация)', required=False )

    class Meta(object):
        model = User
        fields = ('first_name', 'last_name', 'oldpassword', 'password1', 'password2',)
        # TODO: add editing for field 'email'

    def clean_oldpassword(self):
        cd = self.cleaned_data
        #self.instance.set_password('1')
        if cd.get('oldpassword') and not self.instance.check_password(cd['oldpassword']):
            raise ValidationError(u'Неверный пароль.')
        return cd['oldpassword']

    def clean_password1(self):
        cd = self.cleaned_data
        if cd.get('oldpassword') != '' and cd.get('password1') == '':
            raise ValidationError(u'Введите новый пароль')
        return cd['password1']


    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('oldpassword') != '' and cd.get('password2') == '':
            raise ValidationError(u'Введите новый пароль')
        if cd.get('password1') and cd['password1'] != cd['password2']:
            raise ValidationError(u'Пароли не совпадают')
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta(object):
        model = UserProfile
        fields = ('avatar', 'gender', 'birth_date', 'about_me', )
         # TODO: add editing for field 'use_gravatar'