

# plans/serializers.py
from rest_framework import serializers
from accounts.models import Plan
from accounts.models import User

from rest_framework import serializers
from accounts.models import Plan

class PlanSerializer(serializers.ModelSerializer):
    features = serializers.ListField(
        child=serializers.CharField(max_length=200),
        required=True
    )

    class Meta:
        model = Plan
        fields = [
            'id', 'name', 'price', 'duration',
            'features', 'device_limit', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        features_list = validated_data.pop('features', [])
        validated_data['features'] = ', '.join(features_list)
        return Plan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        features_list = validated_data.pop('features', None)
        if features_list is not None:
            instance.features = ', '.join(features_list)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['features'] = [f.strip() for f in instance.features.split(',') if f.strip()]
        return rep

# User-side display
class PlanListSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration', 'features', 'device_limit']

    def get_features(self, obj):
        if obj.features:
            return [f.strip() for f in obj.features.split(',') if f.strip()]
        return []


# If you show the user's current subscribed plan:
class UserPlanSerializer(serializers.ModelSerializer):
    plan = PlanListSerializer()

    class Meta:
        model = User
        fields = ['plan', 'date_joined']


# For User Profile (if needed)
class UserPlanSerializer(serializers.ModelSerializer):
    plan = PlanListSerializer()

    class Meta:
        model = User
        fields = ['plan', 'date_joined']
   


\

