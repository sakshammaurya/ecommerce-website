from django.urls import path
from . import views
from cart.views import *

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('', cart_detail, name='detail'),
    path('checkout/', checkout, name='checkout'),
    path('process-payment/<int:order_id>/', process_payment, name='process_payment'),
    path('order-confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('orders/history/', order_history, name='order_history'),
    

]
