import requests
from lxml import html
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .models import News
from .serializers import NewsSerializer


# Create your views here.
class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    renderer_classes = (TemplateHTMLRenderer,)

    def list(self, request):
        queryset = News.objects.all()
        return Response({'list': queryset}, template_name='list.html')

    def retrieve(self, request, pk=None):
        news = get_object_or_404(self.queryset, pk=pk)
        res = requests.get(news.url)
        tree = html.document_fromstring(res.text)
        content = html.tostring(tree.xpath(
            '//div[@id="story_body_content"]/span')[0]).decode('utf-8')
        # print(content)
        return JsonResponse({'title': news.title, 'page': content})

def article_num(request):
    return JsonResponse({'count': News.objects.count()})
