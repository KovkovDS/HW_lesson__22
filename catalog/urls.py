from django.urls import path
from catalog.apps import CatalogConfig
from .views import (ProductsListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
                    AddedProduct, Contacts, ModerationProductView, custom_permission_denied,
                    FilterCategoryProductsList, )

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='home'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('product/new/', ProductCreateView.as_view(), name='adding_product'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='editing_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='deleting_product'),
    path('product/<int:pk>/added/', AddedProduct.as_view(), name='added_product'),
    path('product/<int:pk>/published/', ModerationProductView.as_view(), name='published_product'),
    path('category_products/<int:id>/', FilterCategoryProductsList.as_view(), name='category_products'),
    # path('error-403/', custom_permission_denied, name='error-403'),
]

handler404 = "catalog.views.page_not_found_view"
