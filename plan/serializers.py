from rest_framework import serializers
from accounts.models import Plan
from accounts.models import User



class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'id', 'name', 'price', 'duration', 'features', 
            'device_limit', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserPlanSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = User
        fields = ['plan', 'date_joined']


# plans/serializers.py


class PlanListSerializer(serializers.ModelSerializer):
    """Serializer for user-side (only active plans)"""
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration', 'features', 'device_limit']