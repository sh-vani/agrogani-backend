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



class UserProfileUpdateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    mobile = serializers.CharField(source='user.mobile', required=False)

    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'email', 'mobile',
            'location', 'language', 'timezone',
            'push_notification', 'advisory_alert',
            'auto_backup', 'share_on_whatsapp'
        ]

    def update(self, instance, validated_data):
        # Update User fields
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
