# models.py
from django.db import models
from django.conf import settings

class Labour(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.mobile})"

class Attendance(models.Model):
    labour = models.ForeignKey(Labour, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('present', 'Present'), ('absent', 'Absent'), ('half_day', 'Half Day')))

    def __str__(self):
        return f"{self.labour.name} - {self.date} - {self.status}"

# class Payment(models.Model):
#     labour = models.ForeignKey(Labour, on_delete=models.CASCADE, related_name='payments')
#     date = models.DateField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     remarks = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.labour.name} - {self.amount} on {self.date}"
