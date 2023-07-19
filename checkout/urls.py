from . import views
from django.urls import path 

urlpatterns = [
    path('',views.checkout, name='checkout'),
]