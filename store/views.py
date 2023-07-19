from django.shortcuts import render
from .models import Product

# Create your views here.


def store(request):
    products = Product.objects.all().filter(is_available = True)
    context = {
        'products' : products,
        
    }
    return render(request, 'homeapp/shop.html', context)

def product_details(request, product_slug):
    try:
        single_product = Product.objects.get(slug = product_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product' : single_product
    }
    return render(request, 'homeapp/single.html', context)