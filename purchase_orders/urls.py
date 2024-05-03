# purchase_orders/urls.py

from django.urls import path
from .views import purchase_order_list, purchase_order_detail

urlpatterns = [
    path('', purchase_order_list, name='purchase_order_list'),
    path('<int:pk>/', purchase_order_detail, name='purchase_order_detail'),
]
