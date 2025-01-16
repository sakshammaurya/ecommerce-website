from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Create your models here.
