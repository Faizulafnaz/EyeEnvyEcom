from . import views
from django.urls import path 

urlpatterns = [
    path('',views.cart, name='cart'),
    path('addcart/<int:product_id>/',views.add_cart, name='addcart'),
    path('removecart/<int:product_id>/',views.remove_cart, name='removecart'),  
    path('deletecart/<int:product_id>/',views.delete_cart, name='deletecart'),  
]   