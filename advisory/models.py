from django.db import models
from django.utils import timezone

created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)

class Advisory(models.Model):  # Renamed from ImportantContact
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    office_address = models.CharField(max_length=255, blank=True, null=True)
    timing = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 🔥
    def __str__(self):
        return self.name



class FertilizerShop(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    hours = models.CharField(max_length=100)
    products = models.TextField()
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)




