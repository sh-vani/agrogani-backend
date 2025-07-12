from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    mobile = serializers.CharField(source='user.mobile', read_only=True)
    plan = serializers.CharField(source='user.plan.name', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'email', 'mobile', 'plan',
             'location', 'language', 'timezone',
            'push_notification', 'advisory_alert',
            'auto_backup', 'share_on_whatsapp'
        ]
