from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'home/product_list.html', {'products': products})

# Create your views here.
