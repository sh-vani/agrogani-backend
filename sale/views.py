# from rest_framework import permissions, status, generics
# from rest_framework.response import Response
# from .models import QuickSale, DetailedSale
# from .serializers import QuickSaleSerializer, DetailedSaleSerializer
# from .permissions import IsPaidMember

# # QUICK SALE ADD
# class QuickSaleAddView(generics.CreateAPIView):
#     queryset = QuickSale.objects.all()
#     serializer_class = QuickSaleSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         return Response({
#             'message': 'Quick sale successfully added',
#             'data': response.data
#         }, status=status.HTTP_201_CREATED)

# # QUICK SALE VIEW
# class QuickSaleListView(generics.ListAPIView):
#     serializer_class = QuickSaleSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return QuickSale.objects.filter(user=self.request.user)

# # DETAILED SALE ADD (PAID MEMBERS ONLY)
# class DetailedSaleAddView(generics.CreateAPIView):
#     queryset = DetailedSale.objects.all()
#     serializer_class = DetailedSaleSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPaidMember]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         return Response({
#             'message': 'Detailed sale successfully added',
#             'data': response.data
#         }, status=status.HTTP_201_CREATED)

# # DETAILED SALE VIEW
# class DetailedSaleListView(generics.ListAPIView):
#     serializer_class = DetailedSaleSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPaidMember]

#     def get_queryset(self):
#         return DetailedSale.objects.filter(user=self.request.user)




from rest_framework import permissions, status, generics
from rest_framework.response import Response
from .models import QuickSale, DetailedSale
from .serializers import QuickSaleSerializer, DetailedSaleSerializer
from .permissions import IsPaidMember  # Assuming ye bana hai







# ✅ Quick Sale Add (sirf add)
class QuickSaleAddView(generics.CreateAPIView):
    serializer_class = QuickSaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            "message": "Quick sale successfully added"
        }, status=status.HTTP_201_CREATED)

# ✅ Detailed Sale Add (sirf add, paid member)
class DetailedSaleAddView(generics.CreateAPIView):
    serializer_class = DetailedSaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            "message": "Detailed sale successfully added"
        }, status=status.HTTP_201_CREATED)

# QUICK SALE VIEW
class QuickSaleListView(generics.ListAPIView):
    serializer_class = QuickSaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuickSale.objects.filter(user=self.request.user)



# DETAILED SALE VIEW
class DetailedSaleListView(generics.ListAPIView):
    serializer_class = DetailedSaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get_queryset(self):
        return DetailedSale.objects.filter(user=self.request.user)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import DetailedSale
from .permissions import IsPaidMember
from django.db.models import Sum

class CropBuyerLedgerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request, buyer_name):
        user = request.user

        # Filter sales by buyer name (case-insensitive)
        sales = DetailedSale.objects.filter(
            user=user,
            buyer_details__buyer_name__iexact=buyer_name
        )

        if not sales.exists():
            return Response({"message": "No sales found for this buyer"}, status=404)

        # Totals
        total_sale = sum(s.total_sale_amount for s in sales)
        total_received = sum(s.payment_details.get("paid_amount", 0) for s in sales)
        total_due = total_sale - total_received
        last_sale = sales.order_by('-sale_date').first()

        # Crop-wise transactions
        transactions = []
        for s in sales:
            for crop in s.crops:
                transactions.append({
                    "crop": crop.get("crop_name"),
                    "bags": crop.get("bags"),
                    "rate": crop.get("rate_per_kg"),
                    "amount": crop.get("total_amount"),
                    "date": s.sale_date
                })

        # Buyer info
        buyer_info = sales.first().buyer_details

        return Response({
            "buyer_name": buyer_info.get("buyer_name"),
            "buyer_mobile": buyer_info.get("buyer_mobile"),
            "market_location": buyer_info.get("market_location"),
            "total_sale_value": total_sale,
            "total_received": total_received,
            "remaining_due": total_due,
            "last_sale_date": last_sale.sale_date if last_sale else None,
            "transactions": transactions
        })


class CropBuyerLedgerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request, buyer_name):
        user = request.user
        sales = DetailedSale.objects.filter(
            user=user,
            buyer_details__buyer_name__iexact=buyer_name
        )

        if not sales.exists():
            return Response({"message": "No sales found for this buyer"}, status=404)

        total_sale = sum(s.total_sale_amount for s in sales)
        total_received = sum(s.payment_details.get("paid_amount", 0) for s in sales)
        total_due = total_sale - total_received
        last_sale = sales.order_by('-sale_date').first()

        transactions = []
        for s in sales:
            for crop in s.crops:
                transactions.append({
                    "crop": crop.get("crop_name"),
                    "bags": crop.get("bags"),
                    "rate": crop.get("rate_per_kg"),
                    "amount": crop.get("total_amount"),
                    "date": s.sale_date
                })

        buyer_info = sales.first().buyer_details

        return Response({
            "buyer": {
                "name": buyer_info.get("buyer_name"),
                "mobile": buyer_info.get("buyer_mobile"),
                "market_location": buyer_info.get("market_location")
            },
            "summary": {
                "total_sale_value": total_sale,
                "total_received": total_received,
                "remaining_due": total_due,
                "last_sale_date": last_sale.sale_date if last_sale else None
            },
            "transactions": transactions
        })



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from collections import defaultdict
from .models import DetailedSale
from .permissions import IsPaidMember

class BuyerLedgerListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        sales = DetailedSale.objects.filter(user=user)

        if not sales.exists():
            return Response({"message": "No sales found"}, status=404)

        ledger = defaultdict(lambda: {
            "buyer_name": "",
            "buyer_mobile": "",
            "market_location": "",
            "total_sale_value": 0,
            "total_received": 0,
            "remaining_due": 0,
            "last_sale_date": None,
            "transactions": []
        })

        for sale in sales:
            buyer = sale.buyer_details.get("buyer_name", "Unknown")
            entry = ledger[buyer]

            entry["buyer_name"] = buyer
            entry["buyer_mobile"] = sale.buyer_details.get("buyer_mobile", "")
            entry["market_location"] = sale.buyer_details.get("market_location", "")
            entry["total_sale_value"] += sale.total_sale_amount
            entry["total_received"] += sale.payment_details.get("paid_amount", 0)
            entry["remaining_due"] = entry["total_sale_value"] - entry["total_received"]

            if not entry["last_sale_date"] or sale.sale_date > entry["last_sale_date"]:
                entry["last_sale_date"] = sale.sale_date

            for crop in sale.crops:
                entry["transactions"].append({
                    "crop": crop.get("crop_name"),
                    "bags": crop.get("bags"),
                    "rate": crop.get("rate_per_kg"),
                    "amount": crop.get("total_amount"),
                    "date": sale.sale_date
                })

        return Response(list(ledger.values()))




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from collections import defaultdict
from .models import DetailedSale
from .permissions import IsPaidMember

class BuyerLedgerSummaryAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated, IsPaidMember]\


    def get(self, request):
        user = request.user
        sales = DetailedSale.objects.filter(user=user)

        if not sales.exists(): 
         return Response({"message": "No sales found"}, status=404)

        total_sale = 0
        total_received = 0
        crop_summary = defaultdict(lambda: {
            "bags": 0,
            "amount": 0
        })
        buyer_names = set()

        for sale in sales:
            total_sale += sale.total_sale_amount
            total_received += sale.payment_details.get("paid_amount", 0)
            buyer_names.add(sale.buyer_details.get("buyer_name", "Unknown"))

            for crop in sale.crops:
                name = crop.get("crop_name", "Unknown")
                crop_summary[name]["bags"] += crop.get("bags", 0)
                crop_summary[name]["amount"] += crop.get("total_amount", 0)

        total_due = total_sale - total_received

        return Response({
            "total_sale_value": total_sale,
            "total_received": total_received,
            "total_due": total_due,
            "total_buyers": len(buyer_names),
            "crop_summary": crop_summary
        })




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from collections import defaultdict
from .models import DetailedSale
from .permissions import IsPaidMember

class CropChartDataAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        sales = DetailedSale.objects.filter(user=user)

        crop_data = defaultdict(lambda: {"bags": 0, "amount": 0})

        for sale in sales:
            for crop in sale.crops:
                name = crop.get("crop_name", "Unknown")
                crop_data[name]["bags"] += crop.get("bags", 0)
                crop_data[name]["amount"] += crop.get("total_amount", 0)

        labels = []
        total_amounts = []
        total_bags = []

        for crop_name, data in crop_data.items():
            labels.append(crop_name)
            total_amounts.append(data["amount"])
            total_bags.append(data["bags"])

        return Response({
            "labels": labels,
            "total_amounts": total_amounts,
            "total_bags": total_bags
        })
