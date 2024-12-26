from django.urls import path
from catalog.apps import CatalogConfig
from .views import home, contacts, product_detail, adding_product, added_product


app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:product_id>/', product_detail, name='product'),
    path('adding_product/', adding_product, name='adding_product'),
    path('added_product/', added_product, name='added_product'),
]
