from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list, object_detail

def user_list(request, params={}, *args, **kwargs):
    params['page'] = 'user_list'
    return HttpResponse('user list')
    #return object_list(request, models.Article.objects.filter(is_staff=False, is_superuser=False), template_name='pages/user_list.html', extra_context=params)

def user_profile(request, user_name=None, params={}, *args, **kwargs):
    params['page'] = 'user_profile'
    if user_name:
        return object_detail(request, User.objects.all(), slug=user_name, slug_field='username', template_name='users/profile.html', extra_context=params)
    else:
        return object_list(request, User.objects.all(), template_name='users/user_list.html', extra_context=params)

def user_creative(request, user_name=None, params={}, *args, **kwargs):
    params['page'] = 'user_creative'
    return HttpResponse('user creative')
    #return object_list(request, models.Article.objects.filter(is_staff=False, is_superuser=False), template_name='pages/user_list.html', extra_context=params)

def marked_by_user(request, user_name=None, params={}, *args, **kwargs):
    params['page'] = 'marked_by_user'
    return HttpResponse('marked by user')
    #return object_list(request, models.Article.objects.filter(is_staff=False, is_superuser=False), template_name='pages/user_list.html', extra_context=params)
