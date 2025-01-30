from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from products.models import Product
from .models import Cart, Order, OrderItem
from django.contrib.auth.decorators import login_required

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


def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user) if request.user.is_authenticated \
           else get_object_or_404(Cart, session_key=request.session.session_key)
    return render(request, 'cart/detail.html', {'cart': cart})

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

def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():  # Ensure database consistency
                # Validate stock
                for item in order.items.all():
                    product = item.product
                    if product.stock_quantity < item.quantity:
                        messages.error(request, 
                            f"Insufficient stock for {product.name}. Only {product.stock_quantity} available.")
                        return redirect('process_payment', order_id=order.id)

                # Process payment
                for item in order.items.all():
                    product = item.product
                    product.stock_quantity -= item.quantity
                    product.save(update_fields=['stock_quantity'])

                # Update order status
                order.status = 'completed'
                order.save(update_fields=['status'])

                # Clear cart session
                if 'cart' in request.session:
                    del request.session['cart']
                    request.session.modified = True  # Force session save

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

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'home/checkout/order_confirmation.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
