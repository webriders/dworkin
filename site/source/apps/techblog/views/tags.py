from django.http import HttpResponse

def tag_cloud(request, params={}, *args, **kwargs):
    params['page'] = 'tag_cloud'
    return HttpResponse('tag cloud')
    #return object_list(request, models.Article.objects.filter(is_staff=False, is_superuser=False), template_name='pages/user_list.html', extra_context=params)
