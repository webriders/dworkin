from django.contrib import admin
from techblog.models import Article, UserProfile


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_public')
    list_editable = ('is_public',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(UserProfile)