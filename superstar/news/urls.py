from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'news', views.NewsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^count/', views.article_num),
    url(r'^create/', views.save_news),
]
