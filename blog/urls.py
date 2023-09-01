from django.contrib import admin
from django.urls import path
from EQHACKSAPP import settings
from . import views

urlpatterns = [
    path('', views.blog_index, name='blog-index'),
    path('post-detail/<slug:slug>/', views.post_detail, name='posts-detail'),
    path('news-updates/<slug:slug>/', views.news_detail, name='news-detail'),
    path('subscribe/', views.subscribe, name='subscribe'),

]