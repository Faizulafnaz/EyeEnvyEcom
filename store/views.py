from django.shortcuts import redirect, render
from .models import Product, Brand
from wishlist.models import Wishlist
from offers.models import Offer
from category.models import Category
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.


def store(request):
    products = Product.objects.all().filter(is_available = True)
    categories = Category.objects.all()
    brand = Brand.objects.all()
    context = {
        'products' : products,
        'categories' : categories,
        'brands' : brand,
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


def filtered_products(request):
    # Retrieve the filter options selected by the user from the URL query parameters
    selected_categories = request.GET.getlist('category')
    selected_brands = request.GET.getlist('brand')
    search_query = request.GET.get('q')


    # Query the database to get the filtered products
    filtered_products = Product.objects.all().filter(is_available = True)
    count = 0
    c = 0
    if search_query:
        count += 1
        filtered_products = filtered_products.filter(
            Q(product_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        c = filtered_products.count()
    if selected_categories:
        filtered_products = filtered_products.filter(category__in=selected_categories)
        c = filtered_products.count()
        count += 1

    if selected_brands:
        filtered_products = filtered_products.filter(brand__in=selected_brands)
        count += 1
        c = filtered_products.count()
    
    if count == 0:
        filtered_products = None

    


    categories = Category.objects.all()
    brand = Brand.objects.all()

    context = {
        'products' : filtered_products,
        'categories' : categories,
        'brands' : brand,
        'c' : c,
        'f': True,
    }

    return render(request, 'homeapp/shop.html', context)


