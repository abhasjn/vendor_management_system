# vendors/urls.py

from django.urls import path
from . import views
from .views import vendor_performance_metrics


urlpatterns = [
    path('', views.vendor_list, name='vendor-list'),
    path('<int:vendor_id>/', views.vendor_detail, name='vendor-detail'),
    path('<int:vendor_id>/performance/', vendor_performance_metrics, name='vendor_performance_metrics'),

]
