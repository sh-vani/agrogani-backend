from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

class QuickSale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100, blank=True, null=True)
    

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    receipt = models.ImageField(upload_to='sales/quick/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} - {self.amount} ₹"

# class DetailedSale(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     sale_date = models.DateField(auto_now_add=True)
#     crops = models.JSONField()  # Example: [{"crop_name": "Wheat", "bags": 10, ...}]
#     transport_details = models.JSONField()
#     buyer_details = models.JSONField()
#     payment_details = models.JSONField()
#     total_sale_amount = models.DecimalField(max_digits=12, decimal_places=2)
#     total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
#     net_income = models.DecimalField(max_digits=12, decimal_places=2)
#     note = models.TextField(blank=True, null=True)
#     receipt = models.ImageField(upload_to='sales/detailed/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Detailed Sale - {self.total_sale_amount} ₹"



class DetailedSale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sale_date = models.DateField()
    
    crops = models.JSONField()  # List of crop dicts
    # Example:
    # [
    #   {"crop_name": "Wheat", "bags": 10, "weight_per_bag": 50, "total_weight": 500, "rate_per_kg": 20, "total_amount": 10000}
    # ]

    transport_details = models.JSONField()
    # Example:
    # {
    #   "vehicle_type": "Truck",
    #   "vehicle_number": "HR26AB1234",
    #   "driver_name": "Ramesh",
    #   "driver_mobile": "9999999999",
    #   "transport_cost": 1000,
    #   "loading_unloading_cost": 500
    # }

    buyer_details = models.JSONField()
    # Example:
    # {
    #   "buyer_name": "Mohan",
    #   "buyer_mobile": "8888888888",
    #   "market_location": "Agra"
    # }

    payment_details = models.JSONField()
    # Example:
    # {
    #   "payment_method": "Cash",
    #   "payment_note": "Paid full"
    # }

    total_sale_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    net_income = models.DecimalField(max_digits=12, decimal_places=2)
    
    note = models.TextField(blank=True, null=True)
    receipt = models.ImageField(upload_to='sales/detailed/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale by {self.user} on {self.sale_date} - ₹{self.total_sale_amount}"
