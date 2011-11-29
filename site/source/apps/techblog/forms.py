# -*- coding: UTF-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from techblog.models import Article, UserProfile
from techblog.widgets import MultiMarkItUpWidget, SelectWithDisabled
from techblog.services.articles import ArticleService

class ArticleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            markup = instance.markup
        else:
            markup = 'html'

        self.fields['short_raw'].widget = MultiMarkItUpWidget(markup_name=markup)
        self.fields['description_raw'].widget = MultiMarkItUpWidget(markup_name=markup)

        self.fields['parent'].widget = forms.HiddenInput()
        self.fields['original'].widget = forms.HiddenInput()

    class Meta(object):
        model = Article
        fields = ('title', 'lang', 'category', 'tags', 'markup', 'short_raw', 'description_raw',
                  'parent', 'original')


class TranslateArticleForm(ArticleForm):

    def __init__(self, *args, **kwargs):
        super(TranslateArticleForm, self).__init__(*args, **kwargs)

        initial = kwargs.get('initial')
        original = initial.get('original')

        self.fields['category'].widget.attrs['disabled'] = True
        self.fields['tags'].widget.attrs['disabled'] = True

        choices = []
        ids = ArticleService.get_all_translations_ids(original)
        for id, value in self.fields['lang'].widget.choices:
            if id in ids:
                value = {'label': value, 'disabled': True}
            choices.append( (id, value) )

        self.fields['lang'].widget = SelectWithDisabled(choices=choices)


class UserForm(forms.ModelForm):
    oldpassword = forms.CharField( widget=forms.PasswordInput, label='Old password', required=False )
    password1 = forms.CharField( widget=forms.PasswordInput, label=u'New password', required=False )
    password2 = forms.CharField( widget=forms.PasswordInput, label=u'New password (verification)', required=False )

    class Meta(object):
        model = User
        fields = ('first_name', 'last_name', 'oldpassword', 'password1', 'password2',)
        # TODO: add editing for field 'email'

    def clean_oldpassword(self):
        cd = self.cleaned_data
        if cd.get('oldpassword') and not self.instance.check_password(cd['oldpassword']):
            raise ValidationError(u'Invalid password.')
        return cd['oldpassword']

    def clean_password1(self):
        cd = self.cleaned_data
        if cd.get('oldpassword') != '' and cd.get('password1') == '':
            raise ValidationError(u'Enter new password')
        return cd['password1']


    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('oldpassword') != '' and cd.get('password2') == '':
            raise ValidationError(u'Enter new password')
        if cd.get('password1') and cd['password1'] != cd['password2']:
            raise ValidationError(u'Passwords does not match')
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta(object):
        model = UserProfile
        fields = ('avatar', 'gender', 'birth_date', 'about_me', )
        # TODO: add editing for field 'use_gravatar'
