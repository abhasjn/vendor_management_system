# vendors/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.vendor_list, name='vendor-list'),
    path('<int:vendor_id>/', views.vendor_detail, name='vendor-detail'),
]
