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




