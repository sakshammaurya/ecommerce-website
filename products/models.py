from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)  # BigInteger primary key
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'products_category'

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(
        'category',
        on_delete=models.CASCADE,
        db_column='category_id',  # Explicit column name for clarity
        null=True,
        blank=True
    )
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
    
    
