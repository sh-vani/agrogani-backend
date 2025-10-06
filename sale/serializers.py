
from decimal import Decimal
from rest_framework import serializers
from .models import QuickSale, DetailedSale
from django.conf import settings



class QuickSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickSale
        fields = ['id', 'crop_name', 'amount', 'note', 'receipt', 'created_at']
        read_only_fields = ['user', 'created_at']



from rest_framework import serializers
from .models import DetailedSale

class BuyerNameSerializer(serializers.ModelSerializer):
    buyer_name = serializers.SerializerMethodField()

    class Meta:
        model = DetailedSale
        fields = ['buyer_name']

    def get_buyer_name(self, obj):
        return obj.buyer_details.get('buyer_name', None)



# from decimal import Decimal
# from rest_framework import serializers
# from .models import DetailedSale
# from shop.models import Buyer

# class DetailedSaleSerializer(serializers.ModelSerializer):
#     buyer_name = serializers.SerializerMethodField()
#     buyer_mobile = serializers.SerializerMethodField()
#     buyer_market_location = serializers.SerializerMethodField()

#     class Meta:
#         model = DetailedSale
#         fields = '__all__'
#         read_only_fields = ['user', 'total_expenses', 'net_income', 'created_at', 'buyer']

#     def get_buyer_name(self, obj):
#         return obj.buyer.name if obj.buyer else obj.buyer_details.get("buyer_name", "Unknown")

#     def get_buyer_mobile(self, obj):
#         return obj.buyer.mobile if obj.buyer else obj.buyer_details.get("buyer_mobile", "")

#     def get_buyer_market_location(self, obj):
#         return obj.buyer.market_location if obj.buyer else obj.buyer_details.get("market_location", "")

#     def create(self, validated_data):
#         buyer_details = validated_data.get('buyer_details', {})
#         buyer_name = buyer_details.get("buyer_name")

#         # ✅ Link or create buyer in Buyer table
#         if buyer_name:
#             buyer_obj, created = Buyer.objects.get_or_create(
#                 name__iexact=buyer_name,  # Case-insensitive match
#                 user=self.context['request'].user,
#                 defaults={
#                     "name": buyer_name,
#                     "mobile": buyer_details.get('buyer_mobile', ''),
#                     "market_location": buyer_details.get('market_location', '')
#                 }
#             )
#             validated_data['buyer'] = buyer_obj

#         # ✅ Calculate expenses and net income
#         transport_details = validated_data.get('transport_details', {})
#         transport_cost = Decimal(str(transport_details.get('transport_cost', 0) or 0))
#         loading_unloading_cost = Decimal(str(transport_details.get('loading_unloading_cost', 0) or 0))
#         total_sale_amount = Decimal(str(validated_data.get('total_sale_amount', 0) or 0))

#         total_expenses = transport_cost + loading_unloading_cost
#         net_income = total_sale_amount - total_expenses

#         validated_data['total_expenses'] = total_expenses
#         validated_data['net_income'] = net_income

#         return super().create(validated_data)


from decimal import Decimal
from rest_framework import serializers
from .models import DetailedSale
from shop.models import Buyer


class DetailedSaleSerializer(serializers.ModelSerializer):
    # Directly accept buyer_id from API
    buyer_id = serializers.PrimaryKeyRelatedField(
        queryset=Buyer.objects.all(),
        source="buyer",
        required=False,
        allow_null=True
    )

    # Extra fields for showing buyer info in response
    buyer_name = serializers.SerializerMethodField()
    buyer_mobile = serializers.SerializerMethodField()
    buyer_market_location = serializers.SerializerMethodField()

    class Meta:
        model = DetailedSale
        fields = '__all__'
        read_only_fields = [
            'user', 'total_expenses', 'net_income',
            'created_at'
        ]

    # -----------------
    # Buyer info fields
    # -----------------
    def get_buyer_name(self, obj):
        return obj.buyer.name if obj.buyer else obj.buyer_details.get("buyer_name", "Unknown")

    def get_buyer_mobile(self, obj):
        return obj.buyer.mobile if obj.buyer else obj.buyer_details.get("buyer_mobile", "")

    def get_buyer_market_location(self, obj):
        return obj.buyer.market_location if obj.buyer else obj.buyer_details.get("market_location", "")

    # -----------------
    # Create Method
    # -----------------
    def create(self, validated_data):
        buyer_details = validated_data.get('buyer_details', {})
        buyer_name = buyer_details.get("buyer_name")

        # If buyer_id already provided -> nothing to do, it's linked automatically
        if not validated_data.get("buyer") and buyer_name:
            # check existing buyer (case-insensitive, same user)
            buyer_obj = Buyer.objects.filter(
                user=self.context['request'].user,
                name__iexact=buyer_name
            ).first()

            if not buyer_obj:
                # create new buyer if not exists
                buyer_obj = Buyer.objects.create(
                    user=self.context['request'].user,
                    name=buyer_name,
                    mobile=buyer_details.get('buyer_mobile', ''),
                    market_location=buyer_details.get('market_location', '')
                )

            validated_data['buyer'] = buyer_obj

        # ✅ Calculate expenses & net income
        transport_details = validated_data.get('transport_details', {})
        transport_cost = Decimal(str(transport_details.get('transport_cost', 0) or 0))
        loading_unloading_cost = Decimal(str(transport_details.get('loading_unloading_cost', 0) or 0))
        total_sale_amount = Decimal(str(validated_data.get('total_sale_amount', 0) or 0))

        total_expenses = transport_cost + loading_unloading_cost
        net_income = total_sale_amount - total_expenses

        validated_data['total_expenses'] = total_expenses
        validated_data['net_income'] = net_income

        return super().create(validated_data)
