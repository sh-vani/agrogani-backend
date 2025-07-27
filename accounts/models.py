from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, default="1 year")
    features = models.TextField()
    device_limit = models.PositiveIntegerField(default=1)  # Default 1 device allowed
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class UserManager(BaseUserManager):
    def create_user(self, email, mobile, full_name, password=None):
        if not email and not mobile:
            raise ValueError("Email or mobile is required")
        user = self.model(
            email=self.normalize_email(email),
            mobile=mobile,
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_otp_verified = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', 'full_name']

    objects = UserManager()

    def __str__(self):
        return self.email or self.mobile

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    mobile_otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Track user's plan
class UserPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):
        return self.plan and self.end_date >= timezone.now()

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"


class RazorpayLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)  # success or failed
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)




 
# Actvity lo



class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.CharField(max_length=50)         # e.g. "Crop", "Sale"
    event_type = models.CharField(max_length=100)    # e.g. "Added Sale"
    description = models.TextField()                 # Summary for frontend
    icon_type = models.CharField(max_length=50, blank=True)
    reference_id = models.CharField(max_length=100, blank=True)
    extra_info = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
        # Optional internal-only
    was_accessed = models.BooleanField(default=False)
    accessed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.module}] {self.user.username} - {self.event_type}"









# from django.db import models
# from django.conf import settings




# class ActivityLog(models.Model):
   
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,  # ✅ This should be used
#         on_delete=models.CASCADE,
#         related_name='activity_logs'
#     )
#     activity_type = models.CharField(max_length=100)  # You can skip choices for flexibility
#     description = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     related_data = models.JSONField(null=True, blank=True)  # Store dynamic key-value info

#     def __str__(self):
#         return f"{self.user.username} - {self.activity_type}"

# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.db import models
# from django.utils import timezone

# class UserManager(BaseUserManager):
#     def create_user(self, email, mobile, full_name, password=None):
#         if not email and not mobile:
#             raise ValueError("Email or mobile is required")
#         user = self.model(
#             email=self.normalize_email(email),
#             mobile=mobile,
#             full_name=full_name
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True, null=True, blank=True)
#     mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
#     full_name = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['mobile', 'full_name']

#     objects = UserManager()

#     def __str__(self):
#         return self.email or self.mobile




