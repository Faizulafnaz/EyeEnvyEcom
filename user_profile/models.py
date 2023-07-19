from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserAddress(models.Model):
    fullname = models.CharField(max_length=100,null=True)
    contact_number = models.CharField(max_length=12,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    house_name = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)


    def __str__(self):
        return self.fullname
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to="userprofile/")
    address = models.CharField(blank=True, max_length=200)
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    phone_no = models.CharField(blank=True, max_length=13)


    def __str__(self) -> str:
        return self.user.first_name