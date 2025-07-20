from django.db import models

class Advisory(models.Model):  # Renamed from ImportantContact
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    office_address = models.CharField(max_length=255, blank=True, null=True)
    timing = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
