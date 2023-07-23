from . import views
from django.urls import path 

urlpatterns = [
    path('',views.store, name='store'),
    path('product/<slug:product_slug>/',views.product_details, name='product_details'),
    path('filtered-product/', views.filtered_products, name='filtered_products'),
]       