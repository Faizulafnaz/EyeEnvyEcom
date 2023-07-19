from django.shortcuts import redirect, render
from user_profile.models import UserAddress
from cart.models import *

# Create your views here.
def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                    print("cart item out of stock")
                    return redirect('cart')
        address = UserAddress.objects.filter(user=request.user)
        context = {
            'addresses':address
        }
    return render(request, "homeapp/checkout.html", context)