from django.contrib import admin
from django.urls import path
from blog_app import views
from django.conf import settings
from django.conf.urls import static


urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.single_post, name='single_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]
