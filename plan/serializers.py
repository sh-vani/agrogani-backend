

# plans/serializers.py
from rest_framework import serializers
from accounts.models import Plan
from accounts.models import User

# accounts/serializers.py


class PlanSerializer(serializers.ModelSerializer):
    features = serializers.ListField(  # ✅ Accept list from frontend
        child=serializers.CharField(),
        write_only=True
    )
    features_display = serializers.SerializerMethodField(read_only=True)  # ✅ Display as list

    class Meta:
        model = Plan
        fields = [
            'id', 'name', 'price', 'duration', 'features', 'features_display',
            'device_limit', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_features_display(self, obj):
        if obj.features:
            return [f.strip() for f in obj.features.split(',') if f.strip()]
        return []

    def to_internal_value(self, data):
        # Convert list to comma-separated string before saving
        if 'features' in data and isinstance(data['features'], list):
            data['features'] = ', '.join(data['features'])
        return super().to_internal_value(data)

    def to_representation(self, instance):
        # Show features as list in response
        representation = super().to_representation(instance)
        representation['features'] = representation.pop('features_display', [])
        return representation


# For User Side (Read-only)
class PlanListSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration', 'features', 'device_limit']

    def get_features(self, obj):
        if obj.features:
            return [f.strip() for f in obj.features.split(',') if f.strip()]
        return []


# For User Profile (if needed)
class UserPlanSerializer(serializers.ModelSerializer):
    plan = PlanListSerializer()

    class Meta:
        model = User
        fields = ['plan', 'date_joined']
   


\

