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


from datetime import date, timedelta
from collections import defaultdict

class BuyerLedgerTodayAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user

        # Get all sales by user
        sales = DetailedSale.objects.filter(user=user).order_by('-sale_date', '-created_at')
        if not sales.exists():
            return Response({"message": "No transactions found"}, status=404)

        # Group transactions by date
        grouped = defaultdict(list)

        for sale in sales:
            sale_date = sale.sale_date
            time_str = sale.created_at.strftime("%I:%M %p") if sale.created_at else "Unknown Time"

            buyer = sale.buyer_details.get("buyer_name", "Unknown")

            # Received Payment
            paid_amount = sale.payment_details.get("paid_amount", 0)
            if paid_amount > 0:
                grouped[sale_date].append({
                    "type": "received",
                    "title": f"Received ₹{paid_amount:,}",
                    "subtitle": f"From: {buyer}",
                    "time": time_str
                })

            # Sold Crops
            for crop in sale.crops:
                crop_name = crop.get("crop_name", "")
                bags = crop.get("bags", 0)
                grouped[sale_date].append({
                    "type": "sold",
                    "title": f"Sold {crop_name} - {bags} bags",
                    "subtitle": f"To: {buyer}",
                    "time": time_str
                })

        # Format response
        response_data = []
        today = date.today()
        yesterday = today - timedelta(days=1)

        for sale_date in sorted(grouped.keys(), reverse=True):
            if sale_date == today:
                label = "Today"
            elif sale_date == yesterday:
                label = "Yesterday"
            else:
                label = sale_date.strftime("%d %b %Y")

            transactions = sorted(grouped[sale_date], key=lambda x: x["time"])

            response_data.append({
                "date": sale_date.strftime("%d %b %Y"),
                "label": label,
                "transactions": transactions
            })

        return Response(response_data)



class CommodityTransactionSummaryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        period = request.query_params.get("period", "today").lower()
        today = date.today()

        # Date range based on period
        if period == "today":
            start_date = end_date = today
        elif period == "week":
            start_date = today - timedelta(days=7)
            end_date = today
        elif period == "month":
            start_date = today.replace(day=1)
            end_date = today
        else:
            return Response({"error": "Invalid period"}, status=400)

        # Primary query
        sales = DetailedSale.objects.filter(
            user=user,
            sale_date__range=[start_date, end_date]
        ).order_by("-sale_date", "-created_at")

        fallback_used = False

        # Fallback if no data
        if not sales.exists():
            latest_sale = DetailedSale.objects.filter(user=user).order_by("-sale_date", "-created_at").first()
            if latest_sale:
                sales = [latest_sale]
                fallback_used = True
            else:
                return Response({"message": "No transactions found"}, status=204)

        transactions = []

        for sale in sales:
            time_str = sale.created_at.strftime("%I:%M %p") if sale.created_at else "Unknown Time"
            date_str = (
                "Today" if sale.sale_date == today else
                "Yesterday" if sale.sale_date == today - timedelta(days=1) else
                sale.sale_date.strftime("%d %b")
            )

            payment_amount = sale.payment_details.get("paid_amount", 0)
            total_amount = sale.total_sale_amount
            if payment_amount == total_amount:
                payment_status = "Paid"
            elif payment_amount == 0:
                payment_status = "Due"
            else:
                payment_status = "Partial"

            for crop in sale.crops:
                transactions.append({
                    "crop_name": crop.get("crop_name", ""),
                    "bags": f"{crop.get('bags', 0)} bags × {crop.get('weight_per_bag', 0)}kg",
                    "rate": f"₹{crop.get('rate_per_kg', 0)}/kg",
                    "date_time": f"{date_str}, {time_str}",
                    "amount": f"₹{crop.get('total_amount', 0)}",
                    "payment_status": payment_status
                })

        return Response({
            "fallback": fallback_used,
            "period": period,
            "transactions": transactions
        })

















# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions
# from collections import defaultdict
# from django.utils.timezone import localtime, now
# from datetime import timedelta
# from django.db.models.functions import TruncDate
# from .models import DetailedSale
# from .permissions import IsPaidMember

# class BuyerLedgerDailyAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated, IsPaidMember]

#     def get(self, request):
#         user = request.user
#         today = localtime(now()).date()
#         yesterday = today - timedelta(days=1)

#         def format_time(dt):
#             return localtime(dt).strftime("%I:%M %p")

#         def get_entries(target_date):
#             # Annotate sale_date to extract just the date part
#             sales = DetailedSale.objects.annotate(
#                 sale_day=TruncDate('sale_date')
#             ).filter(user=user, sale_day=target_date)

#             entries = []

#             for sale in sales:
#                 buyer_name = sale.buyer_details.get("buyer_name", "Unknown")
#                 paid_amount = sale.payment_details.get("paid_amount", 0)

#                 if paid_amount > 0:
#                     entries.append({
#                         "type": "received",
#                         "amount": paid_amount,
#                         "from": buyer_name,
#                         "time": format_time(sale.sale_date)
#                     })

#                 for crop in sale.crops:
#                     entries.append({
#                         "type": "sale",
#                         "crop": crop.get("crop_name"),
#                         "bags": crop.get("bags"),
#                         "to": buyer_name,
#                         "time": format_time(sale.sale_date)
#                     })

#             # Sort by time for consistent ordering
#             return sorted(entries, key=lambda x: x["time"])

#         data = {
#             "today": get_entries(today),
#             "yesterday": get_entries(yesterday)
#         }

#         return Response(data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from collections import defaultdict
from django.utils.timezone import localtime, now
from datetime import timedelta, datetime, date
from .models import DetailedSale
from .permissions import IsPaidMember

class BuyerLedgerDailyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        today = localtime(now()).date()
        yesterday = today - timedelta(days=1)

        def format_time(dt):
            # dt can be date or datetime
            if isinstance(dt, datetime):
                return localtime(dt).strftime("%I:%M %p")
            elif isinstance(dt, date):
                # If only date, show as "12:00 AM" (or use created_at if available)
                return "12:00 AM"
            return ""

        # Group sales by date
        sales = DetailedSale.objects.filter(user=user).order_by('-sale_date', '-created_at')
        grouped = defaultdict(list)

        for sale in sales:
            sale_date = sale.sale_date
            # Prefer created_at time if available and is datetime
            time_str = sale.created_at.strftime("%I:%M %p") if hasattr(sale, "created_at") and sale.created_at else format_time(sale.sale_date)
            buyer = sale.buyer_details.get("buyer_name", "Unknown")

            # Received Payment
            paid_amount = sale.payment_details.get("paid_amount", 0)
            if paid_amount > 0:
                grouped[sale_date].append({
                    "type": "received",
                    "title": f"Received ₹{paid_amount:,}",
                    "subtitle": f"From: {buyer}",
                    "time": time_str
                })

            # Sold Crops
            for crop in sale.crops:
                crop_name = crop.get("crop_name", "")
                bags = crop.get("bags", 0)
                grouped[sale_date].append({
                    "type": "sold",
                    "title": f"Sold {crop_name} - {bags} bags",
                    "subtitle": f"To: {buyer}",
                    "time": time_str
                })

        # Format response as per UI
        response_data = []
        for sale_date in sorted(grouped.keys(), reverse=True):
            if sale_date == today:
                label = "Today"
            elif sale_date == yesterday:
                label = "Yesterday"
            else:
                label = sale_date.strftime("%d %b %Y")

            transactions = sorted(grouped[sale_date], key=lambda x: x["time"])
            response_data.append({
                "date": sale_date.strftime("%d %b %Y"),
                "label": label,
                "transactions": transactions
            })

        return Response(response_data)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from collections import defaultdict
from django.utils.timezone import localtime, now
from django.db.models.functions import TruncDate
from .models import DetailedSale
from .permissions import IsPaidMember

class BuyerLedgerMonthlyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        today = localtime(now()).date()
        first_day = today.replace(day=1)

        # Annotate sale_day and filter by current month
        sales = DetailedSale.objects.annotate(
            sale_day=TruncDate('sale_date')
        ).filter(user=user, sale_day__gte=first_day, sale_day__lte=today)

        ledger_by_date = defaultdict(list)

        def format_time(dt):
            return localtime(dt).strftime("%I:%M %p")

        for sale in sales:
            sale_day = sale.sale_date.strftime("%Y-%m-%d")
            buyer_name = sale.buyer_details.get("buyer_name", "Unknown")
            paid_amount = sale.payment_details.get("paid_amount", 0)

            if paid_amount > 0:
                ledger_by_date[sale_day].append({
                    "type": "received",
                    "amount": paid_amount,
                    "from": buyer_name,
                    "time": format_time(sale.sale_date)
                })

            for crop in sale.crops:
                ledger_by_date[sale_day].append({
                    "type": "sale",
                    "crop": crop.get("crop_name"),
                    "bags": crop.get("bags"),
                    "to": buyer_name,
                    "time": format_time(sale.sale_date)
                })

        # Sort entries within each date
        for date in ledger_by_date:
            ledger_by_date[date] = sorted(ledger_by_date[date], key=lambda x: x["time"])

        return Response(dict(ledger_by_date))

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from collections import defaultdict
from django.utils.timezone import localtime, is_naive, make_aware
from django.db.models.functions import TruncDate
from .models import DetailedSale
from .permissions import IsPaidMember
import datetime

class BuyerLedgerLatestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user

        # Annotate sales with truncated date
        sales = DetailedSale.objects.annotate(
            sale_day=TruncDate('date')
        ).filter(user=user)

        if not sales.exists():
            return Response({"message": "No transactions found"}, status=404)

        # ✅ Use sale_day directly
        latest_date = sales.order_by('day').first().sale_day

        # Filter sales for that date
        latest_sales = sales.filter(sale_day=latest_date)

        ledger = defaultdict(list)

        def format_time(dt):
            # ✅ Ensure it's a datetime, not a date
            if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
                return dt.strftime("%d-%m-%Y")  # fallback format
            if is_naive(dt):
                dt = make_aware(dt)
            return localtime(dt).strftime("%I:%M %p")

        for sale in latest_sales:
            buyer_name = sale.buyer_details.get("buyer_name", "Unknown")
            paid_amount = sale.payment_details.get("paid_amount", 0)

            if paid_amount > 0:
                ledger[str(latest_date)].append({
                    "type": "received",
                    "amount": paid_amount,
                    "from": buyer_name,
                    "time": format_time(sale.sale_date)
                })

            for crop in sale.crops:
                ledger[str(latest_date)].append({
                    "type": "sale",
                    "crop": crop.get("crop_name"),
                    "bags": crop.get("bags"),
                    "to": buyer_name,
                    "time": format_time(sale.sale_date)
                })

        # Sort entries by time
        ledger[str(latest_date)] = sorted(ledger[str(latest_date)], key=lambda x: x["time"])

        return Response(dict(ledger))

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from collections import defaultdict
from .models import DetailedSale
from .permissions import IsPaidMember
from django.utils.dateformat import format as date_format

class BuyerLedgerSummaryAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        sales = DetailedSale.objects.filter(user=user)

        if not sales.exists():
            return Response({"message": "No sales found"}, status=404)

        total_sale = 0
        total_received = 0
     
        last_sale_date = None

        for sale in sales:
            total_sale += sale.total_sale_amount
            total_received += sale.payment_details.get("paid_amount", 0)
           

            if not last_sale_date or sale.sale_date > last_sale_date:
                last_sale_date = sale.sale_date

        total_due = total_sale - total_received

        return Response({
            "total_sale_value": round(total_sale, 2),
            "total_received": round(total_received, 2),
            "total_due": round(total_due, 2),
        
            "last_sale_date": date_format(last_sale_date, "d M Y") if last_sale_date else None
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