from django.shortcuts import render,get_object_or_404
from .models import Product
from django.db.models import Q

#product list handler
def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        # Search in product name OR description (case-insensitive)
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    context = {'products': products}
    return render(request, 'home/product_list.html', context)


# product detail handler
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'home/product_detail.html', {'product': product})

