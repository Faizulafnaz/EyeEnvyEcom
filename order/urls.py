from . import views
from django.urls import path 

urlpatterns = [
    path('',views.place_order, name='placeorder'),
    path('payments/',views.payments, name='payments'),
    path('myorders/',views.my_orders, name='myorders'),
    path('cancelorder/<int:id>',views.cancel_orders, name='cancelorder'),
    path('presuccess/',views.pre_success, name='presuccess'),
    path('success/',views.success, name='success'),
    path('invoice/<int:id>',views.invoice, name='invoice'),
]