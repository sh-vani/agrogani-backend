from rest_framework import serializers
from .models import Advisory  # Renamed import

class AdvisorySerializer(serializers.ModelSerializer):  # Renamed class
    class Meta:
        model = Advisory  # Updated model reference
        fields = '__all__'
