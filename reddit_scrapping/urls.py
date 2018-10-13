"""reddit_scrapping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from comments import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', TemplateView.as_view(template_name='index.html')),
    url('api/fetch_post', views.fetch_posts),
    url('api/start_scraping', views.start_scraping),
    url('api/start', views.start),
    # url('api/fetch_comments', views.fetch_comments),
    # url('api/get_database_posts', views.get_database_posts),
    # url('api/get_database_comments', views.get_database_comments),
    # Serializer

    url('api/Posts/', views.PostListCreate.as_view()),
    url('api/Comments/', views.CommentListCreate.as_view()),
]
