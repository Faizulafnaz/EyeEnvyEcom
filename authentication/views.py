from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
import random
from django.core.mail import send_mail
from django.conf import settings
from cart.views import _session_id
from cart.models import *

# Create your views here.
def signup(request):
    if request.method=="POST":
        get_otp = request.POST.get('otp')
        if not get_otp:
            username = request.POST.get('username')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            phone_no = request.POST.get('phno')

            if not username.strip():
                messages.error(request, "Username is required")
                return redirect('signup')

            if not fname.strip():
                messages.error(request, "First name is required")
                return redirect('signup')

            if not lname.strip():
                messages.error(request, "Last name is required")
                return redirect('signup')

            if not email.strip():
                messages.error(request, "Email is required")
                return redirect('signup')

            if pass1 != pass2:
                messages.error(request, "Passwords do not match")
                return redirect('signup')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken')
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email address is already taken')
                return redirect('signup')
            
            if Profile.objects.filter(mobile=phone_no).exists():
                messages.error(request, 'This Phone Number is already taken')
                return redirect('signup')

            myuser = User.objects.create_user(username=username, email=email, password=pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()
            otp = int(random.randint(1000,9999))
            profile = Profile(user = myuser, mobile = phone_no, otp = otp)
            profile.save()
            mess=f'Hello\t{myuser.username},\nYour OTP to verify your account for EyeEnvy is {otp}\nThanks!'
            send_mail(
            "welcome to EyeEnvy Verify your Email",
            mess,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            fail_silently=False
            )   
            return render(request,'authentication/signup.html',{'otp':True,'usr':myuser})
        else:
            get_email = request.POST.get('email')
            user = User.objects.get(email = get_email)
            if get_otp == Profile.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                messages.success(request,f'Account is created for {user.email}')
                Profile.objects.filter(user=user).delete()
                return redirect(handlelogin)
            else:
               messages.warning(request,f'You Entered a wrong OTP')
               return render(request,'authentication/signup.html',{'otp':True,'usr':user})       
    
    if request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'authentication/signup.html',{'otp':False})

def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")

        user = authenticate(username=username, password=pass1)

        if user is not None:
            try:
                cart = Cart.objects.get(session_id=_session_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    for cart_item in cart_items:
                        cart_item.user = user
                        cart_item.save()
            except:
                pass
            login(request, user)
            return redirect('/')

        else:
            messages.error(request, "Username or password do no match")
            return redirect("handlelogin")

    if request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'authentication/login.html')

def otp_login(request):
    
    if request.method=="POST":
        get_otp = request.POST.get('otp')
        if not get_otp:
            email = request.POST.get('email')
            try:
                user = User.objects.get(email = email)
            except:
                messages.error(request,f"This is not a valid email id")
                return redirect(otp_login)


            if user is not None:
                otp = int(random.randint(1000,9999))
                profile = Profile(user = user, otp = otp)
                profile.save()
                mess=f'Hello\t{user.username},\nYour OTP to Login your account for EyeEnvy is {otp}\nThanks!'
                send_mail(
                "welcome to EyeEnvy Verify your Email for login",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
                )   
                return render(request,'authentication/otp_login.html',{'otp':True,'usr':user})
        else:            
            get_email = request.POST.get('email')
            user = User.objects.get(email = get_email)
            if get_otp == Profile.objects.filter(user=user).last().otp:
                login(request, user)
                messages.success(request,f'Successfully logined {user.email}')
                Profile.objects.filter(user=user).delete()
                return redirect('/')
            else:
               messages.warning(request,f'You Entered a wrong OTP')
               return render(request,'authentication/otp_login.html',{'otp':True,'usr':user})
    if request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'authentication/otp_login.html')        


def handlelogout(request):
    logout(request)
    return HttpResponseRedirect("/")


def forgot_password(request):
     if request.method=="POST":
        get_otp = request.POST.get('otp')
        if not get_otp:
            email = request.POST.get('email')
            try:
                user = User.objects.get(email = email)
            except:
                messages.error(request,f"This is not a valid email id")
                return redirect(forgot_password)


            if user is not None:
                otp = int(random.randint(1000,9999))
                profile = Profile(user = user, otp = otp)
                profile.save()
                mess=f'Hello\t{user.username},\nYour OTP to resetting password for EyeEnvy account - {otp}\nThanks!'
                send_mail(
                "welcome to EyeEnvy Verify your Email for password resetting",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
                )   
                return render(request,'authentication/forgotpassword.html',{'otp':True,'usr':user})
        else:            
            get_email = request.POST.get('email')
            user = User.objects.get(email = get_email)
            if get_otp == Profile.objects.filter(user=user).last().otp:
                Profile.objects.filter(user=user).delete()
                return render(request, 'authentication/resetpassword.html',{'usr':user})
            else:
               messages.warning(request,f'You Entered a wrong OTP')
               return render(request,'authentication/otp_login.html',{'otp':True,'usr':user})
            
     if request.user.is_authenticated:
        return redirect('/')

     return render(request, 'authentication/forgotpassword.html')


def reset_password(request):
    if  request.method == "POST":
        pass1 = request.POST['password']
        pass2 = request.POST["pass1"]

        get_email = request.POST.get('email')
        user = User.objects.get(email = get_email) 
        if pass1 == pass2:
            user.set_password(pass1)
            user.save()
            messages.success(request, 'Password succesfully changed')
            return redirect('handlelogin')
        else:
            messages.error(request, 'passwords not matching')
            return redirect(reset_password)