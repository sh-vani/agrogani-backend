
from rest_framework import serializers
from .models import User, OTP

class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    otp = serializers.CharField()

class SetPasswordSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()



from rest_framework import serializers
from django.utils import timezone

class DashboardHeaderSerializer(serializers.Serializer):
    full_name= serializers.CharField()
    date = serializers.CharField()
    time = serializers.CharField()




from rest_framework import serializers

class WeatherSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    humidity = serializers.IntegerField()
    condition = serializers.CharField()
    wind = serializers.FloatField()





class ForgotPasswordRequestSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField()


class ForgotPasswordVerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    otp = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()


from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)



# # activeite recent
# from rest_framework import serializers
# from .models import ActivityLog


# # serializers.py
# class ActivityLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ActivityLog
#         fields = ["event_type", "description", "module", "icon_type", "timestamp"]


# accounts/serializers.py

from rest_framework import serializers
from .models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    """
    Serializer for the ActivityLog model.
    """
    # Format the timestamp for better readability on the frontend
    timestamp_display = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "event_type",
            "description",
            "module",
            "icon_type",
            "details",
            "timestamp",
            "timestamp_display"
        ]

    def get_timestamp_display(self, obj):
        # Example: "2 hours ago", "Yesterday"
        # You can use django.utils.timesince.timesince here for a "X time ago" format
        from django.utils.timesince import timesince
        return f"{timesince(obj.timestamp)} ago"





#admin dhasboard ka liya framer management


















        
# farmers/serializers.py

from rest_framework import serializers
from django.utils import timezone
from .models import User  # Adjust import path as per your structure

class FarmerSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    status_display = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    plan_end_date = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'email',
            'mobile',
            'location',  # ✅ Now included from model
            'is_active',
            'status_display',
            'plan_name',
            'date_joined',
            'plan_end_date'
        ]

    def get_status_display(self, obj):
        return "Active" if obj.is_active else "Inactive"

    def get_location(self, obj):
        # Return actual location from model (can be null/blank)
        return obj.location or "Not specified"

    def get_plan_end_date(self, obj):
        # Calculate plan end date (365 days from registration)
        if obj.date_joined:
            return obj.date_joined + timezone.timedelta(days=365)
        return None