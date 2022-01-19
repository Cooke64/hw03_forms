from django.urls import path

from .views import *

app_name = 'post'

urlpatterns = [
    path('', index, name='main'),
    path('group/<slug:slug>/', group_posts, name='group'),
    path('profile/<str:username>/', profile, name='profile'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('create/', post_create, name='create'),
]
