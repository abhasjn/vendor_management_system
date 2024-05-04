# vendors/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer
from django.db.models import Count, F, ExpressionWrapper, fields
from purchase_orders.utils import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, calculate_fulfilment_rate



@api_view(['GET', 'POST'])
def vendor_list(request):
    """
    List all vendors or create a new vendor.
    """
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vendor_detail(request, vendor_id):
    """
    Retrieve, update or delete a vendor.
    """
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def vendor_performance_metrics(request, vendor_id):
    """
    Retrieve a vendor's performance metrics.
    """
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Implement logic to fetch performance metrics for the vendor
    
    # Calculate On-Time Delivery Rate
    on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    
    # Calculate Quality Rating Average
    quality_rating_avg = calculate_quality_rating_avg(vendor)
    
    # Calculate Average Response Time
    average_response_time = calculate_average_response_time(vendor)
    
    # Calculate Fulfilment Rate
    fulfilment_rate = calculate_fulfilment_rate(vendor)
    
    # Serialize performance metrics data
    serializer = VendorSerializer({
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfilment_rate': fulfilment_rate
    })
    
    return Response(serializer.data)
