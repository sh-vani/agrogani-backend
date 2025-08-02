# from rest_framework import serializers
# from .models import QuickSale, DetailedSale

# class QuickSaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuickSale
#         fields = '__all__'
#         read_only_fields = ['user', 'created_at']

# class DetailedSaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DetailedSale
#         fields = '__all__'
#         read_only_fields = ['user', 'total_expenses', 'net_income', 'created_at']

#     def create(self, validated_data):
#         transport_details = validated_data.get('transport_details', {})
#         transport_cost = transport_details.get('transport_cost', 0)
#         loading_unloading_cost = transport_details.get('loading_unloading_cost', 0)
#         total_sale_amount = validated_data.get('total_sale_amount', 0)

#         total_expenses = transport_cost + loading_unloading_cost
#         net_income = total_sale_amount - total_expenses

#         validated_data['total_expenses'] = total_expenses
#         validated_data['net_income'] = net_income

#         return super().create(validated_data)

from decimal import Decimal
from rest_framework import serializers
from .models import QuickSale, DetailedSale

class QuickSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickSale
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class DetailedSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailedSale
        fields = '__all__'
        read_only_fields = ['user', 'total_expenses', 'net_income', 'created_at']

    def create(self, validated_data):
        transport_details = validated_data.get('transport_details', {})
        
        # Safely convert to Decimal
        transport_cost = Decimal(str(transport_details.get('transport_cost', 0) or 0))
        loading_unloading_cost = Decimal(str(transport_details.get('loading_unloading_cost', 0) or 0))
        total_sale_amount = Decimal(str(validated_data.get('total_sale_amount', 0) or 0))

        # Calculate using Decimal
        total_expenses = transport_cost + loading_unloading_cost
        net_income = total_sale_amount - total_expenses

        validated_data['total_expenses'] = total_expenses
        validated_data['net_income'] = net_income

        return super().create(validated_data)



from rest_framework import serializers
from .models import DetailedSale

class BuyerNameSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField()

    class Meta:
        model = DetailedSale
        fields = ['buyer_name']

    def get_buyer_name(self, obj):
        return obj.buyer_details.get('buyer_name', None)



