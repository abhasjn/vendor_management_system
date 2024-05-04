from django.db.models import Count, F, Avg, ExpressionWrapper, fields
from .models import PurchaseOrder


def calculate_on_time_delivery_rate(vendor):
    # Query completed purchase orders for the vendor
    completed_po_count = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed'
    ).count()
    
    # Filter purchase orders delivered on or before the delivery date
    on_time_po_count = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
        delivery_date__lte=F('order_date')
    ).count()
    
    # Calculate the on-time delivery rate
    if completed_po_count > 0:
        on_time_delivery_rate = (on_time_po_count / completed_po_count) * 100
    else:
        on_time_delivery_rate = 0.0
    
    return on_time_delivery_rate


def calculate_quality_rating_avg(vendor):
    """
    Calculate the average quality rating for a vendor's purchase orders.
    """
    # Filter completed purchase orders for the vendor
    completed_purchase_orders = vendor.purchaseorder_set.filter(status='completed')
    
    # Calculate the average quality rating
    quality_rating_avg = completed_purchase_orders.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']
    
    return quality_rating_avg


def calculate_average_response_time(vendor):
    """
    Calculate the average response time for a vendor's purchase orders.
    """
    # Filter completed purchase orders with acknowledgment date for the vendor
    completed_purchase_orders = vendor.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
    
    # Calculate the response time for each purchase order
    response_times = completed_purchase_orders.annotate(
        response_time=ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=fields.DurationField()
        )
    )
    
    # Calculate the average response time
    avg_response_time = response_times.aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
    
    return avg_response_time



def calculate_fulfilment_rate(vendor):
    """
    Calculate the fulfilment rate for a vendor's purchase orders.
    """
    # Count the number of completed purchase orders for the vendor
    total_completed_orders = vendor.purchaseorder_set.filter(status='completed').count()
    
    # Count the number of completed purchase orders without issues
    successful_orders = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=True).count()
    
    # Calculate the fulfilment rate
    fulfilment_rate = (successful_orders / total_completed_orders) * 100 if total_completed_orders > 0 else 0
    
    return fulfilment_rate
