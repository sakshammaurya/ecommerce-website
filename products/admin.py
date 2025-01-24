from django.contrib import admin
from .models import Product



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity','image', 'created_at')  # Columns to display
    search_fields = ('name', 'category')  # Searchable fields
    list_filter = ('category', 'created_at')  # Filters in the sidebar
