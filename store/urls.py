from . import views
from django.urls import path 

urlpatterns = [
    path('',views.store, name='store'),
    path('<slug:product_slug>/',views.product_details, name='product_details'),
]   