from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from catalog.models import Product, Contact
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.forms import ProductForm, ContactForm


class ProductsListView(ListView):
    paginate_by = 4
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'


class Contacts(LoginRequiredMixin, ListView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts.html'
    context_object_name = 'contacts'


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = "catalog.view_product"
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


class ModerationProductView(LoginRequiredMixin, View):

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.has_perm('catalog.can_unpublish_product'):
            return PermissionDenied(f'У вас нет прав для публикации Товара "{product.name_p}".')
        product.published = True
        product.save()
        return redirect('catalog:product', pk=product.pk)


class AddedProduct(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "catalog.add_product"
    model = Product
    template_name = 'added_product.html'
    context_object_name = 'added_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        added_product = Product.objects.get(pk=kwargs['pk'])
        context['object'] = added_product
        return context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "catalog.add_product"
    model = Product
    form_class = ProductForm
    template_name = 'adding_product.html'
    success_url = reverse_lazy('catalog:added_product')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        user.groups.add(Group.objects.get(name='Автор карточки продукта'))
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('catalog:added_product', args=[self.object.id], kwargs=self.kwargs)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'editing_product.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        product_for_update = super().get_object(queryset)
        user = self.request.user
        if product_for_update.owner != user and not user.has_perm('catalog.change_product'):
            raise PermissionDenied(f'У вас нет прав для редактирования Товара "{product_for_update.name_p}".')
        return product_for_update

    def get_success_url(self, **kwargs):
        return reverse('catalog:product', args=[self.kwargs.get('pk')])


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        product_for_delete = super().get_object(queryset)
        user = self.request.user
        if product_for_delete.owner != user and not user.has_perm('catalog.delete_product'):
            raise PermissionDenied(f'У вас нет прав для удаления Товара {product_for_delete}".')
        return product_for_delete


def custom_permission_denied(request, exception):
    return render(request, 'error_403.html', {'message': str(exception)})


def page_not_found_view(request, exception):
    return render(request, 'error_403.html', status=404)
