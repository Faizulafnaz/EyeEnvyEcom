from django.shortcuts import redirect, render
import authentication
from user_profile.models import UserAddress, UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.


def add_user_address(request):
    if request.method == "POST":
       name = request.POST['name']
       ph_no = request.POST['ph_no']
       house = request.POST['house']
       landmark = request.POST['landmark']
       district = request.POST['district']
       city = request.POST['city']
       state = request.POST['state']
       country = request.POST['country']
       pincode = request.POST['pincode']


       UserAddress.objects.create(
            fullname = name,
            contact_number = ph_no,
            house_name = house,
            landmark = landmark,
            district = district,
            city = city,
            state = state,
            country = country,
            pincode = pincode,
            user = request.user

       ).save()

       return redirect('placeorder')



def profile(request):
     if request.user.is_authenticated:
          user_address = None
          try:
              user_profile = UserProfile.objects.get(user=request.user)
              user_address = UserAddress.objects.filter(user=request.user)
          except:
              user_profile=UserProfile.objects.create(
                  user = request.user
              ).save()
          context = {
              'user_profile':user_profile,
              'addresses' : user_address,
          }
          return render(request, 'homeapp/profile.html', context)


     
def edit_profile(request):
    if request.method == "POST":
        image = ''
        try:
            image = request.FILES['image']
            user_profile = UserProfile.objects.filter(user=request.user).first()
            user_profile.profile_picture = image
            user_profile.save()
        except:
             pass
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST["country"]
        phone = request.POST["phone"]

        if User.objects.filter(email=email).exists() and email != request.user.email:
                messages.error(request, 'This email address is already taken')
                return redirect(edit_profile)
        
        user_profile = UserProfile.objects.get(user=request.user)
        user = request.user
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.save()
        user_profile.address = address
        user_profile.city = city
        user_profile.state = state
        user_profile.country = country
        user_profile.phone_no = phone
        user_profile.save()

        messages.success(request, 'Your details updated')
        return redirect(profile)


def change_password(request):
    if request.method == "POST":
        password = request.POST['password']
        npass1 = request.POST['npass1']
        npass2 = request.POST['npass2']
        user = request.user
        
        
        if npass1 != npass2:
            messages.error(request, 'Password not matching')
            return redirect(change_password)
        
        success = user.check_password(password)
        if success:
            user.set_password(npass1)
            user.save()
            messages.success(request, 'Password succesfully changed')
            return redirect('handlelogout')
        else:
            messages.error(request, 'Incorrect Password')
            return redirect(change_password)
        
    return render(request, 'homeapp/changepassword.html')


def edit_address(request, id):
    if request.method == "POST":
       name = request.POST['fname']
       ph_no = request.POST['no']
       house = request.POST['house']
       landmark = request.POST['landmark']
       district = request.POST['district']
       city = request.POST['city']
       state = request.POST['state']
       country = request.POST['country']


       UserAddress.objects.filter(id=id).update(
            fullname = name,
            contact_number = ph_no,
            house_name = house,
            landmark = landmark,
            district = district,
            city = city,
            state = state,
            country = country,

       )
       messages.success(request, 'saved changes')
       return redirect(edit_address, id)
    address = UserAddress.objects.get(id=id)
    context = {
        'address' : address,
    }
    return render(request, "homeapp/address.html", context)