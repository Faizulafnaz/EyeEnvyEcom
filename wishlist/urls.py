from . import views
from django.urls import path 

urlpatterns = [
    path('',views.wishlist, name='wishlist'),
    path('<int:id>/',views.add_wishlist, name='add_wishlist'),
    path('delete/<int:id>/',views.delete_wishlist, name='delete_wishlist'),
]