from django.http import HttpResponse

from django.views.generic import TemplateView
from techblog.service.tags import TagService

class TagsList(TemplateView):
    template_name = 'tags/tags_list.html'

    def get_context_data(self, **kwargs):
        context = super(TagsList, self).get_context_data(**kwargs)
        context['categories'] = TagService.get_category_tag_cloud()
        context['page'] = 'tags_page'
        return context

#def tag_cloud(request, params={}, *args, **kwargs):
#    params['page'] = 'tag_cloud'
#    return HttpResponse('tag cloud')
#    #return object_list(request, models.Article.objects.filter(is_staff=False, is_superuser=False), template_name='pages/user_list.html', extra_context=params)
