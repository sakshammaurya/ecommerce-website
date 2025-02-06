from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from django.db.models import Q
from django.core.paginator import Paginator

#product list handler
def product_list(request):
    # Fetch all categories
    categories = Category.objects.only('id', 'name')

    # Fetch products
    products = Product.objects.select_related('category').only('id', 'name', 'price', 'image', 'category_id')

    # Filtering
    category_slug = request.GET.get('category')
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)

    # Product search filter
    product_filter = request.GET.get('product_filter')
    if product_filter:
        products = products.filter(
            Q(name__icontains=product_filter) |
            Q(description__icontains=product_filter)
        )

    # Sorting
    DEFAULT_SORT_BY = 'created_at'
    sort_by = request.GET.get('sort_by', DEFAULT_SORT_BY)
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # default sorting by newest
        products = products.order_by('-created_at')

    # Paginate products
    paginator = Paginator(products, 20)  # Show 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    sort_labels = {
    'created_at': 'Newest',
    'price_asc': 'Price: Low to High',
    'price_desc': 'Price: High to Low',
    'name': 'Name'
    }

    context = {
        'categories': categories,
        'page_obj': page_obj,
        'current_category': category_slug,
        'current_sort': sort_by,
        'current_filter': product_filter,
        'sort_labels': sort_labels,
    }

    return render(request, 'home/product_list.html', context)

# product detail handler
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'home/product_detail.html', {'product': product})

