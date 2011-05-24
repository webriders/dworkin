from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.list_detail import object_list, object_detail
from techblog.models import UserProfile

class UserProfilesList(ListView):
    model = UserProfile
    context_object_name = 'user_profiles'
    template_name = 'users/userprofile_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfilesList, self).get_context_data(**kwargs)
        context['page'] = 'users_page'
        return context

class UserProfileDetail(DetailView):
    context_object_name = 'profile'
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        user_name = self.kwargs['user_name']
        return UserProfile.objects.all().get(user__username=user_name)

    def get_context_data(self, **kwargs):
        user = self.request.user
        user_name = self.kwargs['user_name']
        context = super(UserProfileDetail, self).get_context_data(**kwargs)
        context['page'] = 'user_profile'
        context['edit_allowed'] = user.is_authenticated() and user.username == user_name
        return context


def user_creative(request, user_name=None, params={}, *args, **kwargs):
    params['page'] = 'user_creative'
    return HttpResponse('user creative')
    #return object_list(request, models.Article.objects.filter(is_staff=False, is_superuser=False), template_name='pages/user_list.html', extra_context=params)

def marked_by_user(request, user_name=None, params={}, *args, **kwargs):
    params['page'] = 'marked_by_user'
    return HttpResponse('marked by user')
    #return object_list(request, models.Article.objects.filter(is_staff=False, is_superuser=False), template_name='pages/user_list.html', extra_context=params)
