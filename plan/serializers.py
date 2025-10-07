

# plans/serializers.py
from rest_framework import serializers
from accounts.models import Plan
from accounts.models import User

class PlanSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    limitations = serializers.SerializerMethodField()
    
    class Meta:
        model = Plan
        fields = [
            'id', 'name', 'price', 'duration', 'features', 
            'limitations', 'device_limit', 'is_active', 'is_recommended',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_features(self, obj):
        # Convert comma-separated string to list
        if obj.features:
            return [f.strip() for f in obj.features.split(',') if f.strip()]
        return []

    def get_limitations(self, obj):
        # Convert comma-separated string to list
        if obj.limitations:
            return [l.strip() for l in obj.limitations.split(',') if l.strip()]
        return []



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