from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import redirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from techblog.models import UserProfile
from techblog.forms import UserProfileForm, UserForm


class UserProfilesList(ListView):
    queryset = UserProfile.objects.all()
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
        user_name = self.kwargs.get('user_name') or self.request.user.username
        user_profile = get_object_or_404(UserProfile, user__username=user_name, user__is_active=True)
        return user_profile

    def get_context_data(self, **kwargs):
        user = self.request.user
        user_name = self.kwargs.get('user_name') or self.request.user.username
        context = super(UserProfileDetail, self).get_context_data(**kwargs)
        context['page'] = 'users_page'
        context['sub_page'] = 'user_profile'
        context['edit_allowed'] = user.is_authenticated() and user.username == user_name
        return context


class UserProfileEdit(TemplateView):
    template_name = 'users/profile_edit.html'

    def get(self, request, *args, **kwargs):
        user =  request.user
        context = {}
        context['page'] = 'users_page'
        context['sub_page'] = 'user_profile'

        if user.is_authenticated():
            user_profile = UserProfile.objects.get(user=user)

            context['is_authenticated'] = True
            context['UserForm'] = UserForm(instance=user)
            context['UserProfileForm'] = UserProfileForm(instance=user_profile)
        else:
            context['is_authenticated'] = False

        return self.render_to_response(context)

    def post(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        user_form = UserForm(request.POST, request.FILES, instance=user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and user_profile_form.is_valid():
            password2 = user_form.cleaned_data['password2']
            if password2:
                user.set_password(password2)
            user_form.save()
            user_profile_form.save()
            return redirect('/profile/')

        context = {}
        context['is_authenticated'] = True
        context['UserForm'] = user_form
        context['UserProfileForm'] = user_profile_form

        return self.render_to_response(context=context)


def marked_by_user(request, user_name=None, params={}, *args, **kwargs):
    params['page'] = 'marked_by_user'
    return HttpResponse('marked by user')
    #return object_list(request, models.Article.objects.filter(is_staff=False, is_superuser=False), template_name='pages/user_list.html', extra_context=params)
