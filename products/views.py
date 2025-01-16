from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import Product

from .serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

# Create your views here.
