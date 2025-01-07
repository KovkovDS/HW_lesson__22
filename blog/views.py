from blog.models import BlogArticle
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView


class BlogArticlesListView(ListView):
    paginate_by = 4
    model = BlogArticle
    template_name = 'blog/home.html'
    context_object_name = 'articles'


# class Contacts(ListView):
#     model = Contact
#     template_name = 'contacts.html'
#     context_object_name = 'contacts'


class BlogArticleDetailView(DetailView):
    model = BlogArticle
    template_name = 'blog/article.html'
    context_object_name = 'article'


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
        added_article = self.object
        return "{0}?param={1}".format(success_url, added_article)
