from django.urls import path
from blog.apps import BlogConfig
from .views import BlogArticlesListView, BlogArticleDetailView, AddedBlogArticle, BlogArticleCreateView


app_name = BlogConfig.name

urlpatterns = [
    path('', BlogArticlesListView.as_view(), name='home'),
    path('article/<int:pk>/', BlogArticleDetailView.as_view(), name='article'),
    path('adding_article/', BlogArticleCreateView.as_view(), name='adding_article'),
    path('added_article/', AddedBlogArticle.as_view(), name='added_article'),
    ]
