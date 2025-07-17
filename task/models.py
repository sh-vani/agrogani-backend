from django.db import models

# Create your models here.
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

class Task(models.Model):
    PRIORITY_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
    CATEGORY_CHOICES = [
        ('Irrigation', 'Irrigation'),
        ('Fertilization', 'Fertilization'),
        ('Harvesting', 'Harvesting'),
        ('Planting', 'Planting'),
        ('Maintenance', 'Maintenance'),
        ('Other', 'Other'),
    ]
    REPEAT_CHOICES = [('None', 'None'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Custom', 'Custom')]

    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    crop = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    reminder = models.CharField(max_length=50, default='At time of task')  # radio: 15 min, 1 hr, etc.
    assigned_to = models.CharField(max_length=100)  # optional: later relate to user/labour table
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    weather_sensitive = models.BooleanField(default=False)
    details = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_recurring = models.BooleanField(default=False)
    repeat_type = models.CharField(
    max_length=20,
    choices=[('None', 'None'), ('Daily', 'Daily'), ('Weekly', 'Weekly')],
    default='None'
)



