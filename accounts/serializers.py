
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



# activeite recent
from rest_framework import serializers
from .models import ActivityLog


# serializers.py
class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ["event_type", "description", "module", "icon_type", "timestamp"]
