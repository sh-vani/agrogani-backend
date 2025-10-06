from rest_framework import serializers
from .models import Advisory  , FertilizerShop

class AdvisorySerializer(serializers.ModelSerializer):  # Renamed class
    class Meta:
        model = Advisory  # Updated model reference
        fields = '__all__'


from rest_framework import serializers

class FertilizerShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = FertilizerShop
        fields = '__all__'





