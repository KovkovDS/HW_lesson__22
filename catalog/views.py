from catalog.models import Product, Contact
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView


class ProductsListView(ListView):
    paginate_by = 4
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'


class Contacts(ListView):
    model = Contact
    template_name = 'contacts.html'
    context_object_name = 'contacts'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


class AddedProduct(TemplateView):
    model = Product
    template_name = 'added_product.html'
    context_object_name = 'added_product'


class ProductCreateView(CreateView):
    model = Product
    fields = ['name_p', 'price_by', 'description_p', 'picture', 'category']
    template_name = 'adding_product.html'
    success_url = reverse_lazy('catalog:added_product')

    def get_success_url(self, **kwargs):
        success_url = super().get_success_url()
        added_product = self.object
        return "{0}?param={1}".format(success_url, added_product)
