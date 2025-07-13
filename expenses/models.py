from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Expense(models.Model):
    EXPENSE_TYPES = [
        ('labour', 'Labour Payment'),
        ('fertilizer', 'Fertilizer & Pesticide Invoice'),
        ('seed', 'Seed Invoice'),
        ('equipment', 'Equipment Expense'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('bank', 'Bank'),
    ]

    PAYMENT_TYPE = [
        ('cash', 'Cash'),
        ('credit', 'Credit'),
          ('advance', 'Advance'),
    ('regular', 'Regular'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crop = models.CharField(max_length=100)
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    date = models.DateField()
    paying_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=10)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=10)
    note = models.TextField(blank=True, null=True)
    bill_photo = models.ImageField(upload_to='bills/', blank=True, null=True)
    bill_no = models.CharField(max_length=20, unique=True, blank=True)

    # Optional fields
    labour_name = models.CharField(max_length=100, blank=True, null=True)
    work_description = models.TextField(blank=True, null=True)
    daily_wage = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    shop = models.ForeignKey('shop.Shop', on_delete=models.SET_NULL, null=True, blank=True)
    seed_name = models.CharField(max_length=100, blank=True, null=True)

    equipment_name = models.CharField(max_length=100, blank=True, null=True)
    equipment_type = models.CharField(max_length=20, blank=True, null=True)
    vendor_name = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.bill_no:
            from datetime import datetime
            today_str = datetime.now().strftime("%Y%m%d")
            last_id = Expense.objects.filter(bill_no__startswith=today_str).count() + 1
            self.bill_no = f"{today_str}{last_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.expense_type} | {self.paying_amount} | {self.bill_no}"
