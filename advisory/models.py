from django.db import models

# Create your models here.
from django.db import models
# from django.contrib.auth.models import User
class Advisory(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    crop_type = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    location = models.CharField(max_length=255)
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title
