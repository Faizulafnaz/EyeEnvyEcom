from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Product, Wishlist
from offers.models import Offer
from category.models import Category
from django.contrib.auth.decorators import login_required

# Create your views here.
#-------------------------------------wishlist----------------------------------------------

@login_required(login_url='handlelogin')
def wishlist(request):
    usr = request.user.id
    try:
        products = Wishlist.objects.filter(user = usr)
    except:
        products = ''  
    return render(request,'homeapp/wishlist.html',{'wishlisted':products})


@login_required
def add_wishlist(request, id):
    user = request.user
    try:
        wishlist = Wishlist.objects.get(user=user, product=id)
    except Wishlist.DoesNotExist:
        product = Product.objects.get(id=id)
        wishlist = Wishlist(user=user,  product=product)
        wishlist.save()
    messages.success(request,'Item added to wishlist')
    try:
        product = Product.objects.get(id = id)
    except Exception as e:
        raise e
    return redirect('product_details', product.slug)

def delete_wishlist(request, id):
    usr = request.user.id
    product = Wishlist.objects.get(user = usr ,product = id)
    product.delete()
    return redirect(wishlist)