from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Order, OrderItem
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
#product list handler
def product_list(request):
    products = Product.objects.all()
    return render(request, 'home/product_list.html', {'products': products})

# product detail handler
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'home/product_detail.html', {'product': product})

#add to cart handler
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided

        # Validate quantity
        if quantity < 1:
            messages.error(request, "Invalid quantity.")
            return redirect('product_detail', product_id=product_id)

        # Get or initialize the cart in the session
        cart = request.session.get('cart', {})
        product_key = str(product_id)  # Session keys are strings

        # Update quantity if product exists in cart, else add it
        if product_key in cart:
            cart[product_key] += quantity
        else:
            cart[product_key] = quantity

        # Save the updated cart back to the session
        request.session['cart'] = cart
        messages.success(request, f"Added {quantity} × {product.name} to your cart.")
        return redirect('product_detail', product_id=product_id)

    # Redirect to product detail if request is not POST
    return redirect('product_detail', product_id=product_id)

#checkout handler
def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, "Your cart is empty!")
        return redirect('product_list')  # Redirect to product listing
    
    if request.method == 'POST':
        # Process the order
        try:
            order = Order.objects.create(
                email=request.POST.get('email'),
                shipping_address=request.POST.get('shipping_address'),
                total=0  # Will be calculated below
            )
            
            total = 0
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=int(product_id))
                item_total = product.price * quantity
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                total += item_total
            
            order.total = total
            order.save()
            #redirect to payment page
            return redirect('process_payment', order_id=order.id)
        
        except Exception as e:
            messages.error(request, f"Error processing order: {str(e)}")
    
    # Calculate cart total for display
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=int(product_id))
        item_total = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total
        })
        total += item_total
    
    return render(request, 'home/checkout/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


#payment gateway 
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        try:
            # Validate stock
            for item in order.items.all():
                product = item.product
                if product.quantity < item.quantity:
                    messages.error(request, 
                        f"Insufficient stock for {product.name}. Only {product.quantity} available.")
                    return redirect('process_payment', order_id=order.id)

            # Process payment
            for item in order.items.all():
                product = item.product
                product.quantity -= item.quantity
                product.save()

            # Update order status
            order.status = 'completed'
            order.save()

            # Clear cart
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True

            return redirect('order_confirmation', order_id=order.id)

        except Exception as e:
            messages.error(request, f"Payment failed: {str(e)}")
            return redirect('process_payment', order_id=order.id)

    # GET request - Show payment form
    return render(request, 'home/checkout/process_payment.html', {
        'order': order,
        'cart_items': order.items.all(),
        'total': order.total
    })
#order confirmation after sucessful payment
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'home/checkout/order_confirmation.html', {'order': order})

