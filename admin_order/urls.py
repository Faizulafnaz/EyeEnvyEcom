from django.urls import path
from . import views

urlpatterns = [
    path('order_details/',views.order_details, name='orderdetails'),
    path('order_manage/<int:id>',views.order_manage, name='ordermanage'),

]