

# plans/serializers.py
from rest_framework import serializers
from accounts.models import Plan
from accounts.models import User



# serializers.py

class PlanSerializer(serializers.ModelSerializer):
    # ✅ Accept list from frontend
    features = serializers.ListField(
        child=serializers.CharField(max_length=200),
        write_only=True
    )
    # ✅ Display as list in API response
    features_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Plan
        fields = [
            'id', 'name', 'price', 'duration', 'features', 'features_display',
            'device_limit', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_features_display(self, obj):
        """Convert stored string back to list for API response."""
        if obj.features:
            try:
                return [f.strip() for f in obj.features.split(',') if f.strip()]
            except:
                return []
        return []

    def to_internal_value(self, data):
        """
        Convert incoming list to comma-separated string for model.
        """
        if 'features' in data and isinstance(data['features'], list):
            # Join list items into a single comma-separated string
            data['features'] = ', '.join(data['features'])
        return super().to_internal_value(data)

    def to_representation(self, instance):
        """
        Customize output: show features as list.
        """
        ret = super().to_representation(instance)
        # Replace 'features' (which is now a string) with the list version
        ret['features'] = ret.pop('features_display', [])
        return ret




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

