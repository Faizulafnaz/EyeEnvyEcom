from . import views
from django.urls import path 

urlpatterns = [
    path('add_user_address/',views.add_user_address, name='adduseraddress'),
    path('profile/',views.profile, name='profile'),
    path('editprofile/',views.edit_profile, name='editprofile'),
    path('changepassword/',views.change_password, name='changepassword'),
    path('editaddress/<int:id>',views.edit_address, name='editaddress'),
]   