from blog.models import BlogArticle
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class BlogArticlesListView(ListView):
    paginate_by = 4
    model = BlogArticle
    template_name = 'blog/home.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)


class BlogArticleDetailView(DetailView):
    model = BlogArticle
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self, **kwargs):
        self.object = super().get_object(**kwargs)
        self.object.number_views += 1
        self.object.save()
        return self.object


class AddedBlogArticle(TemplateView):
    model = BlogArticle
    template_name = 'blog/added_article.html'
    context_object_name = 'added_article'


class BlogArticleCreateView(CreateView):
    model = BlogArticle
    fields = ['title', 'content', 'preview', 'published']
    template_name = 'blog/adding_article.html'
    success_url = reverse_lazy('blog:added_article')

    def get_success_url(self, **kwargs):
        success_url = super().get_success_url()
        return "{0}?param={1}".format(success_url, self.kwargs.get('pk'))


class BlogArticleUpdateView(UpdateView):
    model = BlogArticle
    fields = ['title', 'content', 'preview', 'published']
    template_name = 'blog/editing_article.html'
    success_url = reverse_lazy('blog:home')

    def get_success_url(self, **kwargs):
        return reverse('blog:article', args=[self.kwargs.get('pk')])


class BlogArticleDeleteView(DeleteView):
    model = BlogArticle
    template_name = 'blog/articles_confirm_delete.html'
    success_url = reverse_lazy('blog:home')
