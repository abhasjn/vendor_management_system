# purchase_orders/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from django.db.models import Count, F, ExpressionWrapper, fields,Avg
from django.utils import timezone


@api_view(['GET', 'POST'])
def purchase_order_list(request):
    """
    List all purchase orders or create a new purchase order.
    """
    if request.method == 'GET':
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_detail(request, pk):
    """
    Retrieve, update or delete a purchase order.
    """
    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Calculate On-Time Delivery Rate
            completed_po_count = PurchaseOrder.objects.filter(
                vendor=purchase_order.vendor,
                status='completed'
            ).count()
            on_time_po_count = PurchaseOrder.objects.filter(
                vendor=purchase_order.vendor,
                status='completed',
                delivery_date__lte=F('order_date')
            ).count()
            on_time_delivery_rate = (on_time_po_count / completed_po_count) * 100

            # Update the vendor's On-Time Delivery Rate
            purchase_order.vendor.on_time_delivery_rate = on_time_delivery_rate
            purchase_order.vendor.save()

            # Calculate Quality Rating Average
            completed_po_quality_avg = PurchaseOrder.objects.filter(
                vendor=purchase_order.vendor,
                status='completed',
                quality_rating__isnull=False
            ).aggregate(quality_rating_avg=Avg('quality_rating'))['quality_rating_avg']

            # Update the vendor's Quality Rating Average
            purchase_order.vendor.quality_rating_avg = completed_po_quality_avg
            purchase_order.vendor.save()

            # Calculate Average Response Time
            avg_response_time = PurchaseOrder.objects.filter(
                vendor=purchase_order.vendor,
                acknowledgment_date__isnull=False
            ).aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time']

            # Update the vendor's Average Response Time
            purchase_order.vendor.average_response_time = avg_response_time
            purchase_order.vendor.save()

            # Calculate Fulfilment Rate
            fulfilled_po_count = PurchaseOrder.objects.filter(
                vendor=purchase_order.vendor,
                status='completed',
                quality_rating__isnull=False
            ).count()
            total_po_count = PurchaseOrder.objects.filter(
                vendor=purchase_order.vendor
            ).count()
            fulfilment_rate = (fulfilled_po_count / total_po_count) * 100

            # Update the vendor's Fulfilment Rate
            purchase_order.vendor.fulfilment_rate = fulfilment_rate
            purchase_order.vendor.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)