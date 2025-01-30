from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, "Account created successfully.")
        return redirect('login')  # Redirect to login page

    return render(request, 'home/signup.html')  # Render signup form


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.user.is_authenticated:
        # Merge session cart with user cart
                try:
                    session_cart = Cart.objects.get(session_key=request.session.session_key)
                    user_cart, created = Cart.objects.get_or_create(user=request.user)
                    
                    for item in session_cart.items.all():
                        user_item, created = user_cart.items.get_or_create(
                            product=item.product,
                            defaults={'quantity': item.quantity, 'price': item.price}
                        )
                        if not created:
                            user_item.quantity += item.quantity
                            user_item.save()
                    session_cart.delete()
                except Cart.DoesNotExist:
                    pass
            return redirect('home') # Redirect to your homepage
    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

