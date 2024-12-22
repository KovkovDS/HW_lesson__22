from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_c')
    search_fields = ('name_c', 'description_c')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_p', 'price_by', 'category')
    list_filter = ('category',)
    search_fields = ('name_p', 'description_p')