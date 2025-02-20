from django.contrib.auth.mixins import LoginRequiredMixin
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


class AddedProduct(LoginRequiredMixin, TemplateView):
    model = Product
    template_name = 'added_product.html'
    context_object_name = 'added_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        added_product = Product.objects.get(pk=kwargs['pk'])
        context['object'] = added_product
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'adding_product.html'
    success_url = reverse_lazy('catalog:added_product')

    def get_success_url(self, **kwargs):
        return reverse('catalog:added_product', args=[self.object.id], kwargs=self.kwargs)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'editing_product.html'
    success_url = reverse_lazy('catalog:home')

    def get_success_url(self, **kwargs):
        return reverse('catalog:product', args=[self.kwargs.get('pk')])


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
