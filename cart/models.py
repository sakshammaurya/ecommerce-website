from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='carts'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_cart'  # New table name

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'cart_cartitem'  # New table name

    @property
    def total_price(self):
        return self.price * self.quantity

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        identifier = self.user.username if self.user else self.session_key
        return f"Cart ({identifier})"
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='orders'
    )
    cart = models.OneToOneField(
        Cart,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    email = models.EmailField()
    shipping_address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name if self.product else '[deleted product]'}"

