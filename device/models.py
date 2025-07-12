# from django.db import models

# # Create your models here.
from django.db import models
from accounts.models import User

# class Device(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     device_id = models.CharField(max_length=255)
#     registered_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.email} - {self.device_id}"




# from django.db import models
# from django.contrib.auth import get_user_model



class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    device_id = models.CharField(max_length=255)  # Example: IMEI, UUID, etc.
    device_name = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.device_id}"
