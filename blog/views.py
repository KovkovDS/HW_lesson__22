from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from blog.forms import BlogArticleForm
from blog.models import BlogArticle
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.conf import settings

from catalog.models import Category
from catalog.services import ListProductsCategories


class BlogArticlesListView(ListView):
    paginate_by = 4
    model = BlogArticle
    template_name = 'blog/home.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        category_products = self.request.GET.get('category.id')
        context['categories'] = categories
        context['products'] = ListProductsCategories.get_products_categories(category_products)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.has_perm('blog.view_blogarticle'):
            return queryset.filter(published=True)
        return queryset


class BlogArticleDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = "blog.view_blogarticle"
    model = BlogArticle
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self, **kwargs):
        self.object = super().get_object(**kwargs)
        self.object.number_views += 1
        self.object.save()
        if self.object.number_views >= 100:
            send_mail('У статьи более 100 просмотров',
                      f'У статьи {self.object.title} более 100 просмотров, поздравляю! :)',
                      settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
        return self.object


class AddedBlogArticle(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "blog.add_blogarticle"
    model = BlogArticle
    template_name = 'blog/added_article.html'
    context_object_name = 'added_article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        added_article = BlogArticle.objects.get(pk=kwargs['pk'])
        context['added_article'] = added_article
        return context


class BlogArticleCreateView(LoginRequiredMixin, CreateView):
    model = BlogArticle
    form_class = BlogArticleForm
    template_name = 'blog/adding_article.html'
    success_url = reverse_lazy('blog:added_article')

    def get_object(self, queryset=None):
        article_for_adding = super().get_object(queryset)
        user = self.request.user
        if not user.has_perm('blog.add_blogarticle'):
            raise PermissionDenied(f'У вас нет прав для добавления Статьи "{article_for_adding.title}".')
        return article_for_adding

    def get_success_url(self, **kwargs):
        return reverse('blog:added_article', args=[self.object.id], kwargs=self.kwargs)


class PublicationBlogArticleView(LoginRequiredMixin, View):

    def post(self, request, pk):
        article = get_object_or_404(BlogArticle, pk=pk)
        if not request.user.has_perm('blog.can_publish_blogarticle'):
            return PermissionDenied(f'У вас нет прав для публикации Статьи "{article.title}".')
        article.published = True
        article.save()
        return redirect('blog:home')


class BlogArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogArticle
    form_class = BlogArticleForm
    template_name = 'blog/editing_article.html'
    success_url = reverse_lazy('blog:home')

    def get_object(self, queryset=None):
        article_for_update = super().get_object(queryset)
        user = self.request.user
        if not user.has_perm('blog.change_blogarticle'):
            raise PermissionDenied(f'У вас нет прав для редактирования Статьи "{article_for_update.title}".')
        return article_for_update

    def get_success_url(self, **kwargs):
        return reverse('blog:article', args=[self.kwargs.get('pk')])


class BlogArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogArticle
    template_name = 'blog/articles_confirm_delete.html'
    success_url = reverse_lazy('blog:home')

    def get_object(self, queryset=None):
        article_for_delete = super().get_object(queryset)
        user = self.request.user
        if not user.has_perm('blog.delete_blogarticle'):
            raise PermissionDenied(f'У вас нет прав для удаления Статьи "{article_for_delete.title}".')
        return article_for_delete


def custom_permission_denied(request, exception):
    return render(request, 'error_403.html', {'message': str(exception)})
