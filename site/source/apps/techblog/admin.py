from django.contrib import admin
from django.contrib.auth.models import User
from  django.contrib.admin.sites import NotRegistered
from techblog.models import Article, UserProfile, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_public', 'date')
    list_editable = ('is_public',)
    list_filter = ('author', 'is_public',)
    date_hierarchy = 'date'

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



try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, UserAdmin)