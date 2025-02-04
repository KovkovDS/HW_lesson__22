from django.urls import path
from catalog.apps import CatalogConfig
from .views import (ProductsListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
                    AddedProduct, Contacts)


app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='home'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('product/new/', ProductCreateView.as_view(), name='adding_product'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='editing_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='deleting_product'),
    path('product/<int:pk>/added/', AddedProduct.as_view(), name='added_product'),
]
