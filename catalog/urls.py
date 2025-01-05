from django.urls import path
from catalog.apps import CatalogConfig
from .views import ProductsListView, ProductDetailView, ProductCreateView, AddedProduct, Contacts


app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='home'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('adding_product/', ProductCreateView.as_view(), name='adding_product'),
    path('added_product/', AddedProduct.as_view(), name='added_product'),
]
