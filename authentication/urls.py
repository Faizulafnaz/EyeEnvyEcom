from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.handlelogin, name='handlelogin'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.handlelogout, name='handlelogout'),
    path('otp_login/',views.otp_login, name='otp_login'),
    path('forgotpassword/',views.forgot_password, name='forgotpassword'),
    path('resetpassword/',views.reset_password, name='resetpassword'),
]
