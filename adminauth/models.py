from django.db import models

# Create your models here.
# adminauth/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class AdminUser(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


    # ✅ Add this property — required by Django auth system
    @property
    def is_authenticated(self):
        return True  # Custom user is always authenticated if exists

    # Optional: Add these for compatibility
    @property
    def is_anonymous(self):
        return False