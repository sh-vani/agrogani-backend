from rest_framework import serializers
from .models import Buyer, Sale

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'crop', 'quantity', 'rate', 'total_value', 'received_amount', 'sale_date', 'status']

    def get_status(self, obj):
        if obj.received_amount >= obj.total_value:
            return "✅ Paid"
        elif obj.received_amount > 0:
            return "🟠 Partial"
        else:
            return "🔴 Due"
