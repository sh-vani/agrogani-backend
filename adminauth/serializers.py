# adminauth/serializers.py
from rest_framework import serializers
from .models import AdminUser

class AdminSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = AdminUser
        fields = ['full_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        admin = AdminUser(**validated_data)
        admin.set_password(validated_data['password'])
        admin.save()
        return admin
