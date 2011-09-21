# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from  django.contrib.admin.sites import NotRegistered
from techblog.models import Article, UserProfile, Category


class ArticleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'get_authors', 'is_public', 'date')
    list_editable = ('is_public',)
    list_filter = ('authors', 'is_public',)
    date_hierarchy = 'date'

    def get_authors(self, obj):
        return ', '.join(str(author) for author in obj.authors.all())
    get_authors.short_description = u'Список авторов'

admin.site.register(Article, ArticleAdmin)

class CategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'get_full_name', 'date_joined', 'is_active',)
    date_hierarchy = 'date_joined'
    list_filter = ('is_active',)



try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, UserAdmin)