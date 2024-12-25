from django.contrib import admin
from .models import Category, Product, Contact

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_c')
    search_fields = ('name_c', 'description_c')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_p', 'price_by', 'category', 'updated_at', 'description_p')
    list_filter = ('category',)
    search_fields = ('name_p', 'description_p')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'legal_address', 'mailing_address', 'email', 'tel')
