from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User  # या जहाँ तुम्हारा User model है वहां से import करो

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  
    location = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=50, default='English')
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    push_notification = models.BooleanField(default=True)
    advisory_alert = models.BooleanField(default=False)
    auto_backup = models.BooleanField(default=True)
    share_on_whatsapp = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} Profile"
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from userprofile.models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
