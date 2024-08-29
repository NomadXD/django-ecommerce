from django.shortcuts import render
from .models import Product

def home(request):
    featured_products = Product.objects.all()[:4]  # Get 4 featured products
    return render(request, 'store/home.html', {'featured_products': featured_products})

def product_catalog(request):
    products = Product.objects.all()
    return render(request, 'store/product_catalog.html', {'products': products})