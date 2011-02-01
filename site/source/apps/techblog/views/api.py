from django.http import HttpResponse, HttpResponseForbidden
from techblog.functions import html_parser

def parse_html(request):
    if request.user.is_authenticated():
        return HttpResponse(html_parser(request.POST.get('data', '')))
    else:
        return HttpResponseForbidden()
