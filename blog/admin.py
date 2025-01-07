from django.contrib import admin
from .models import BlogArticle


@admin.register(BlogArticle)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_at', 'published', 'number_views')
    list_filter = ('title', 'create_at', 'published',)
    search_fields = ('title',)
