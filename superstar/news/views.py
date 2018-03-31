import os

import requests
from lxml import html
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template import loader
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from .models import News
from .serializers import NewsSerializer
from superstar.settings import BASE_DIR


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


def save_news(request):
    news = News(title="test_5", url="http://www.test.com/5")
    news.save()
    return JsonResponse({"message": "saved"})


@receiver(post_save, sender=News)
def print_receiver(sender, **kwargs):
    print("Received signal!")
    user = "PC"
    dynamic_data = "Django"
    html_message = loader.render_to_string(
            os.path.join(BASE_DIR, 'news/templates/html_mail.html'),
            {
                'user_name': user,
                'subject':  'Thank you from ' + dynamic_data,
            }
        )
    send_mail("Django Mail",
              "Message",
              "non_exist@msn.com",
              ["emmalover@gmail.com"],
              html_message=html_message
              )
