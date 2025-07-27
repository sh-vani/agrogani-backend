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





# from rest_framework import serializers
# from .models import Region, Advisory, ServiceProvider

# class RegionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Region
#         fields = '__all__'

# class AdvisorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Advisory
#         fields = '__all__'

# class ServiceProviderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ServiceProvider
#         fields = '__all__'
