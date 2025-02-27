from django.urls import path
from blog.apps import BlogConfig
from catalog.views import custom_permission_denied
from .views import (BlogArticlesListView, BlogArticleDetailView, AddedBlogArticle, BlogArticleCreateView,
                    BlogArticleUpdateView, BlogArticleDeleteView, PublicationBlogArticleView)


app_name = BlogConfig.name

urlpatterns = [
    path('', BlogArticlesListView.as_view(), name='home'),
    path('article/<int:pk>/', BlogArticleDetailView.as_view(), name='article'),
    path('article/new/', BlogArticleCreateView.as_view(), name='adding_article'),
    path('article/<int:pk>/edit/', BlogArticleUpdateView.as_view(), name='editing_article'),
    path('article/<int:pk>/delete/', BlogArticleDeleteView.as_view(), name='deleting_article'),
    path('article/<int:pk>/added/', AddedBlogArticle.as_view(), name='added_article'),
    path('article/<int:pk>/published/', PublicationBlogArticleView.as_view(), name='published_article'),
    # path('error-403/', custom_permission_denied, name='error-403'),
    ]

handler404 = "catalog.views.page_not_found_view"
