from rest_framework import serializers
from accounts.models import Plan
from accounts.models import User

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration', 'features', 'device_limit']

class UserPlanSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = User
        fields = ['plan', 'date_joined']
