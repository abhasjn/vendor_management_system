# purchase_orders/models.py

from django.db import models
from vendors.models import Vendor
import json

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.TextField()  # Use TextField to store JSON data
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.po_number

    def get_items_as_dict(self):
        return json.loads(self.items)

    def set_items_as_dict(self, items_dict):
        self.items = json.dumps(items_dict)


# blank=True:
# This parameter allows the field to be left blank in forms. 
# In Django, blank=True is used for form validation, indicating that the field is not required to have a value when submitting a form. 
# If a form is submitted without providing a value for this field, it will be considered valid.

# models.ForeignKey(Vendor, ...): This part of the line defines the type of field. 
# In this case, it's a foreign key field, which means it establishes a many-to-one relationship between the PurchaseOrder model and the Vendor model.
# It links each PurchaseOrder instance to a single Vendor instance.

# on_delete=models.CASCADE: This parameter specifies the behavior to adopt when the referenced Vendor is deleted. 
# In this case, models.CASCADE means that when a Vendor is deleted, 
# all associated PurchaseOrder instances will also be deleted.
# This ensures referential integrity in the database, preventing orphaned PurchaseOrder records that reference nonexistent Vendor records.