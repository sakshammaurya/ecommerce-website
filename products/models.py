from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STOCK_STATUS = (
        (0, 'Out of Stock'),
        (1, 'Low Stock'),
        (2, 'In Stock'),
    )
    
    stock_status = models.IntegerField(choices=STOCK_STATUS, default=2)
    
    def __str__(self):
        return self.name
    
    def get_stock_status_display(self):
        return dict(self.STOCK_STATUS)[self.stock_status]






