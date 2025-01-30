from django.shortcuts import render,get_object_or_404
from .models import Product


#product list handler
def product_list(request):
    products = Product.objects.all()
    return render(request, 'home/product_list.html', {'products': products})

# product detail handler
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'home/product_detail.html', {'product': product})


