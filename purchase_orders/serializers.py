# purchase_orders/serializers.py

from rest_framework import serializers
from .models import PurchaseOrder

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'  # Include all fields of the PurchaseOrder model
