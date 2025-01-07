from django.urls import path
from blog.apps import BlogConfig
from .views import (BlogArticlesListView, BlogArticleDetailView, AddedBlogArticle, BlogArticleCreateView,
                    BlogArticleUpdateView, BlogArticleDeleteView)


app_name = BlogConfig.name

urlpatterns = [
    path('', BlogArticlesListView.as_view(), name='home'),
    path('article/<int:pk>/', BlogArticleDetailView.as_view(), name='article'),
    path('article/new/', BlogArticleCreateView.as_view(), name='adding_article'),
    path('article/<int:pk>/edit/', BlogArticleUpdateView.as_view(), name='editing_article'),
    path('article/<int:pk>/delete/', BlogArticleDeleteView.as_view(), name='deleting_article'),
    path('article/added/', AddedBlogArticle.as_view(), name='added_article'),
    ]
