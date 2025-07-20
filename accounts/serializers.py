
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
