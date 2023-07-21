from . import views
from django.urls import path 

urlpatterns = [
    path('addoffer/',views.add_offer, name='addoffer'),
    path('addcoupon/',views.add_coupon, name='addcoupon'),
]