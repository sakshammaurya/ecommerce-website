from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'date_added')  # Columns to display
    search_fields = ('name', 'category')  # Searchable fields
    list_filter = ('category', 'date_added')  # Filters in the sidebar
