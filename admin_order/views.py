from django.shortcuts import render
from order.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='admin_login')
def order_details(request):
    order_items = OrderItem.objects.all()
    context = {
        'order_items' : order_items,
    }
    return render(request, 'adminpanel/page-orders-1.html', context)

@login_required(login_url='admin_login')
def order_manage(request, id):
    cart_item = OrderItem.objects.get(id = id )
    if request.method == "POST":
        status = request.POST['status']
        cart_item.status= status
        cart_item.save()
    context = {
        'cart_item' : cart_item,
    }
    return render(request, "adminpanel/ordermanage.html", context)