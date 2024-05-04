# vendors/serializers.py

from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)  # Make name field optional
    contact_details = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    vendor_code = serializers.CharField(required=False)

    
    class Meta:
        model = Vendor
        fields = '__all__'
