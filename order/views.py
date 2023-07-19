from django.http import HttpResponse
from django.shortcuts import redirect, render
from user_profile.models import UserAddress
from cart.models import *
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import razorpay
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def payments(request, total = 0):

    # saving payment details
    if request.user.is_authenticated:
        payment_method = PaymentMethod.objects.get(id=1)
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
        )
        payment.save()
        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order.payment = payment
        order.status = 'accepted'
        order.save()

        # move cart items to ordered items
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            orderitem = OrderItem(
                user = request.user,
                order = order,
                product = cart_item.product,
                payment = payment,
                product_price = cart_item.product.price,
                quantity = cart_item.quantity,
                status = 'accepted',
            )
            orderitem.save()

            total += cart_item.sub_total()


    
        # Reduce stock of ordered product
            product = Product.objects.get(id=cart_item.product.id)
            product.stock -= cart_item.quantity
            product.save()
        
        # order message
        mess=f'Hello\t{request.user.username},\nYour Order of { order.order_id } has confirmed.\nThanks!'
        send_mail(
        "Thank you for the order",
        mess,
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False
        )
        # Removing Cart items
        CartItem.objects.filter(user=request.user).delete()   

        return render(request, "homeapp/confirm.html")

    return render(request, 'homeapp/payment.html') 


def place_order(request):
    if request.user.is_authenticated:
        current_user = request.user
        total = 0
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                print("cart item out of stock")
                return redirect('cart')
            total += ((cart_item.product.price) * (cart_item.quantity))
        if cart_count <= 0:
            return redirect('store')

        if request.method == "POST":
            addr = request.POST['address']
            address = UserAddress.objects.get(id=addr)
        else:
            address = UserAddress.objects.filter(user=current_user).order_by('-id').first() 

        data = Order()
        data.user = current_user
        data.address = address
        data.order_total = total
        data.save()
        order = Order.objects.get(user = current_user, status=data.status, order_id=data.order_id)
        
        client = razorpay.Client(auth= ( settings.KEY, settings.KEY_SECRET ))
        payment = client.order.create({'amount' :total * 100 , 'currency' :'INR', 'payment_capture' : 1 })
        


        context = {
            'order' : order,
            'cart_items' : cart_items,
            'total' : total,
            'payment' : payment,
        }
        return render(request,'homeapp/payment.html', context)
    
def my_orders(request):
    myorders = OrderItem.objects.filter(Q(user=request.user) & ~Q(status='pending'))
    context = {
        "myorders":myorders,
    }
    return render(request, 'homeapp/myorders.html', context)


def cancel_orders(request, id):
     
    item = OrderItem.objects.get(id = id)
    item.status = 'cancelled'
    quantity = item.quantity
    item.product.stock += quantity
    item.save()

    current_user = request.user
    subject = "Cancell order succesfull!"
    mess = f'Greetings {current_user.first_name}.\nYour Order {item.order.order_id} has been cancelled. \nThank you for shopping with us!'
    send_mail(
            subject,
            mess,
            settings.EMAIL_HOST_USER,
            [current_user.email],
            fail_silently = False
    )
    return redirect(my_orders)


# after razorpay payment

# this method that redirecting from razorpay webiste. this method will redirect to success function
@csrf_exempt
def pre_success(request):
    return redirect(success)


# for order confirmation page and adding payment details
def success(request, total = 0):
        payment_method = PaymentMethod.objects.get(id=2)
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
            status = 'Paid'
        )
        payment.save()
        order = Order.objects.filter(user=request.user).order_by('-id').first()
        order.payment = payment
        order.status = 'accepted'
        order.save()
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            orderitem = OrderItem(
                user = request.user,
                order = order,
                product = cart_item.product,
                payment = payment,
                product_price = cart_item.product.price,
                quantity = cart_item.quantity,
                status = 'accepted',
            )
            orderitem.save()

            total += cart_item.sub_total()


    
        # Reduce stock of ordered product
            product = Product.objects.get(id=cart_item.product.id)
            product.stock -= cart_item.quantity
            product.save()
        
        # order message
        mess=f'Hello\t{request.user.username},\nYour Order of { order.order_id } has confirmed.\nThanks!'
        send_mail(
        "Thank you for the order",
        mess,
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False
        )
        # Removing Cart items
        CartItem.objects.filter(user=request.user).delete()   
        return render(request, "homeapp/confirm.html")


# invoice function
def invoice(request, id):

    # id from user side(my orders)
    order_item = OrderItem.objects.get(id = id)
    # for retreving the order
    order = Order.objects.get(order_id = order_item.order.order_id)
    # for retreving all ordered items in that order
    order_items = OrderItem.objects.filter(order = order)
    context = {
        'order':order,
        'order_items':order_items,

    }
    return render(request, 'homeapp/invoice.html', context)
