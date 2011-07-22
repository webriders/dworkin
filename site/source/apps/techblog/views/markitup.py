from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from techblog.services.articles import ArticleService

class MarkitupPreviewer(TemplateView):
    template_name = "markitup/article_preview.html"

    def get_context_data(self, **kwargs):
        context = super(MarkitupPreviewer, self).get_context_data(**kwargs)

        markup = self.args[0]
        data = self.request.POST.get("data")

        context["rendered_data"] = ArticleService.render_markup(markup, data)
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return login_required( super(MarkitupPreviewer, self).dispatch )(request, *args, **kwargs)
