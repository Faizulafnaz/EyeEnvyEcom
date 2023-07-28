from django.shortcuts import render, redirect
from .models import Offer, Coupon
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# for adding a new offer
@login_required(login_url='admin_login')
def add_offer(request):
    if request.method == "POST":
        name = request.POST['name']
        percentage = request.POST['perc']
        start_date = request.POST['start-date']
        end_date = request.POST['end-date']

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(add_offer)

        offer = Offer.objects.create(
            name = name,
            off_percent = percentage,
            start_date = start_date,
            end_date = end_date,
        )
        offer.save()
        messages.success(request,f'Offer "{name}" created')
        return redirect(add_offer)
    offer = Offer.objects.all()
    context = {
        'offers' : offer,
    }
    return render(request, "adminpanel/offer.html", context)


#for adding new coupons----------------------------------------------
@login_required(login_url='admin_login')
def add_coupon(request):
    if request.method == "POST":
        name = request.POST['name']
        percentage = request.POST['perc']
        min_amount = request.POST['min']
        max_discount = request.POST['max']
        end_date = request.POST['end-date']

        coupon = Coupon.objects.create(
            coupon_code = name,
            off_percent = percentage,
            min_amount = min_amount,
            max_discount = max_discount,
            expiry_date = end_date,
        )
        coupon.save()
        messages.success(request,f'Coupon "{name}" created')
        return redirect(add_coupon)
    coupon = Coupon.objects.all()
    context = {
        'coupons' : coupon,
    }
    return render(request, "adminpanel/coupon.html", context)