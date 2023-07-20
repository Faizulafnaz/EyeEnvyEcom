from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product
from django.contrib import messages
from offers.models import Coupon
from .models import Cart,CartItem

# Create your views here.

# Collecting session id
def _session_id(request):
    cart = request.session.session_key

    # if user is not loggined
    if not cart:
        cart = request.session.create()
    return cart


# for adding products to the cart

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    try:
        cart = Cart.objects.get(session_id=_session_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            session_id = _session_id(request)
        )
    cart.coupon = None
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if ((product.stock)-(cart_item.quantity + 1)) < 0:
            messages.warning(request, "")
            return redirect('cart')
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            if ((product.stock)- 1) < 0:
                print('hi') 
                return redirect('cart')
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1, 
                cart = cart,
                user = request.user,
            )
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1, 
                cart = cart,
            )
            cart_item.save()
    return redirect('cart')

# for reducing cart item quantity
def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(session_id=_session_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


#for removing cart item 
def delete_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(session_id=_session_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')
                       

# For showing cart items on cart page 

def cart(request, total=0, quantity=0, cart_items=None,count=0,coupons=None, cart=None, discount_amount=0):

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            coupons = Coupon.objects.all()
        else:
            cart = Cart.objects.get(session_id = _session_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items:
            if cart_item.product.offer:
                total += cart_item.sub_total_with_offer()
            elif cart_item.product.category.offer:
                total += cart_item.sub_total_with_offer_category()
            else:
                total += cart_item.sub_total()

            quantity += cart_item.quantity
            count += 1
    except:
        pass
    
    # for adding coupons
    if request.method == "POST":
        coup = request.POST['search']
        try:
            coupon = Coupon.objects.get(coupon_code = coup)
            if coupon.is_expired():
                messages.error(request, 'Coupon is expired')
                return redirect('cart')
            
            if coupon.min_amount > total:
                messages.error(request, f'Amount should be greater than {coupon.min_amount}')
                return redirect('cart')
            
            cart = Cart.objects.get(session_id = _session_id(request))

            discount_amount = total * coupon.off_percent / 100

            if discount_amount > coupon.max_discount:
                discount_amount = coupon.max_discount

            total -= discount_amount
            cart.coupon = coupon
            cart.save()
                
        except:
            messages.error(request, 'Coupon not found')
            return redirect('cart')

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'count': count,
        'coupons': coupons,
        'cart':cart,
        'discount_amount':discount_amount,
    }

    return render(request, "homeapp/cart.html", context)