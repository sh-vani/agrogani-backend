from django.db import models
from django.conf import settings

class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    device_limit = models.PositiveIntegerField(default=1)
    allowed_crop_types = models.JSONField(default=list)  # Example: ["type1", "type2"]

    def __str__(self):
        return self.name

class Crop(models.Model):
    CROP_TYPE_CHOICES = (
        ("type1", "Type 1"),
        ("type2", "Type 2"),
    )
    IRRIGATION_CHOICES = (
        ("Canal", "Canal"),
        ("Tubewell", "Tubewell"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    crop_name = models.CharField(max_length=100)
    field_size = models.DecimalField(max_digits=10, decimal_places=2)
    field_unit = models.CharField(max_length=20)  # Acres, Bigha, hectares
    crop_type = models.CharField(max_length=10, choices=CROP_TYPE_CHOICES)
    sowing_date = models.DateField()
    irrigation_source = models.CharField(max_length=10, choices=IRRIGATION_CHOICES)
    additional_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} - {self.field_name}"
