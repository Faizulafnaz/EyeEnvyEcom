from django.shortcuts import redirect, render
from .models import Product
from wishlist.models import Wishlist
from offers.models import Offer
from category.models import Category
from django.contrib.auth.decorators import login_required


# Create your views here.


def store(request):
    products = Product.objects.all().filter(is_available = True)
    try:
        pass
    except:
        pass
    context = {
        'products' : products,
        
    }
    return render(request, 'homeapp/shop.html', context)

def product_details(request, product_slug):
    is_wish = None
    single_product = None
    try:
        single_product = Product.objects.get(slug = product_slug)
        
    except Exception as e:
        raise e
    
    try:
        if request.user.is_authenticated:
            is_wish =  Wishlist.objects.get(user=request.user, product=single_product)
    except:
        pass

    
    context = {
        'single_product' : single_product,
        'is_wish': is_wish,
    }
    return render(request, 'homeapp/single.html', context)



