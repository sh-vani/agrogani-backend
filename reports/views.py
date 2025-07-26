

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPaidMember
from sale.models import QuickSale, DetailedSale
from expenses.models import Expense
from django.db.models import Sum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import month_name

class SummaryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        today = datetime.today()
        month = int(month) if month else today.month
        year = int(year) if year else today.year

        # Current month summary
        start_date = datetime(year, month, 1).date()
        end_date = today.date() if month == today.month else datetime(year, month + 1, 1).date()

        quick_sale = QuickSale.objects.filter(
            user=user, created_at__date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

        detailed_sale = DetailedSale.objects.filter(
            user=user, sale_date__range=[start_date, end_date]
        ).aggregate(total=Sum('total_sale_amount'))['total'] or 0

        total_revenue = quick_sale + detailed_sale

        total_expense = Expense.objects.filter(
            user=user, date__range=[start_date, end_date]
        ).aggregate(total=Sum('paying_amount'))['total'] or 0

        profit = total_revenue - total_expense

        # Last 12 months graph data
        graph_data = []
        for i in range(12):
            ref_date = today - relativedelta(months=11 - i)
            m_start = datetime(ref_date.year, ref_date.month, 1).date()
            m_end = (m_start + relativedelta(months=1))

            q_sale = QuickSale.objects.filter(
                user=user, created_at__date__range=[m_start, m_end]
            ).aggregate(total=Sum('amount'))['total'] or 0

            d_sale = DetailedSale.objects.filter(
                user=user, sale_date__range=[m_start, m_end]
            ).aggregate(total=Sum('total_sale_amount'))['total'] or 0

            revenue = q_sale + d_sale

            expense = Expense.objects.filter(
                user=user, date__range=[m_start, m_end]
            ).aggregate(total=Sum('paying_amount'))['total'] or 0

            graph_data.append({
                "month": month_name[m_start.month],
                "year": m_start.year,
                "revenue": round(revenue, 2),
                "expenses": round(expense, 2),
                "profit": round(revenue - expense, 2)
            })

        return Response({
            "month": month,
            "year": year,
            "total_revenue": round(total_revenue, 2),
            "total_expense": round(total_expense, 2),
            "profit": round(profit, 2),
            "graph_data": graph_data
        })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPaidMember
from crop.models import Crop
from sale.models import QuickSale, DetailedSale
from expenses.models import Expense
from django.db.models import Sum




class CropWiseReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        crops = Crop.objects.filter(user=user)
        report = []

        for crop in crops:
            crop_name = crop.crop_name

            # Revenue from QuickSale
            quick_sale = QuickSale.objects.filter(
                user=user,
                crop_name__iexact=crop_name
            ).aggregate(total=Sum('amount'))['total'] or 0

            # Revenue from DetailedSale (loop through JSONField)
            detailed_sale_total = 0
            detailed_sales = DetailedSale.objects.filter(user=user)
            for sale in detailed_sales:
                for item in sale.crops:
                    if item.get("crop_name", "").lower() == crop_name.lower():
                        detailed_sale_total += item.get("total_amount", 0)

            revenue = quick_sale + detailed_sale_total

            # Investment from Expense
            investment = Expense.objects.filter(
                user=user,
                crop_name__iexact=crop_name
            ).aggregate(total=Sum('paying_amount'))['total'] or 0

            # Profit & ROI
            profit = revenue - investment
            roi = round((profit / investment) * 100, 2) if investment > 0 else 0

            report.append({
                "crop_name": crop.crop_name,
                "field_name": crop.field_name,
                "field_size": f"{crop.field_size} {crop.field_unit}",
                "crop_type": crop.crop_type,
                "investment": round(investment, 2),
                "revenue": round(revenue, 2),
                "profit": round(profit, 2),
                "roi": roi
            })

        return Response(report)



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsPaidMember
# from crop.models import Crop
# from sale.models import QuickSale, DetailedSale
# from expenses.models import Expense
# from django.db.models import Sum

# class CropWiseReportAPIView(APIView):
#     permission_classes = [IsAuthenticated, IsPaidMember]

#     def get(self, request):
#         user = request.user
#         crops = Crop.objects.filter(user=user)
#         report = []

#         for crop in crops:
#             crop_name = crop.crop_name

#             # Revenue from QuickSale
#             quick_sale = QuickSale.objects.filter(
#                 user=user,
#                 crop_name__iexact=crop_name
#             ).aggregate(total=Sum('amount'))['total'] or 0

#             # Revenue from DetailedSale (loop through JSONField)
#             detailed_sale_total = 0
#             detailed_sales = DetailedSale.objects.filter(user=user)
#             for sale in detailed_sales:
#                 for item in sale.crops:
#                     if item.get("crop_name", "").lower() == crop_name.lower():
#                         detailed_sale_total += item.get("total_amount", 0)

#             revenue = quick_sale + detailed_sale_total

#             # ✅ Fixed: Investment from Expense
#             investment = Expense.objects.filter(
#                 user=user,
#                 crop__crop_name__iexact=crop_name  # Corrected field lookup
#             ).aggregate(total=Sum('amount'))['total'] or 0

#             # Profit & ROI
#             profit = revenue - investment
#             roi = round((profit / investment) * 100, 2) if investment > 0 else 0

#             report.append({
#                 "crop_name": crop.crop_name,
#                 "field_name": crop.field_name,
#                 "field_size": f"{crop.field_size} {crop.field_unit}",
#                 "crop_type": crop.crop_type,
#                 "investment": round(investment, 2),
#                 "revenue": round(revenue, 2),
#                 "profit": round(profit, 2),
#                 "roi": roi
#             })

#         return Response(report)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPaidMember
from crop.models import Crop
from sale.models import QuickSale, DetailedSale
from expenses.models import Expense
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .permissions import IsPaidMember

class CropDetailReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPaidMember]

    def get(self, request, crop_id):
        user = request.user
        crop = get_object_or_404(Crop, id=crop_id, user=user)
        crop_name_key = crop.crop_name.strip().lower()

        # 🔍 Investment Breakdown by expense_type
        expense_types = ['Seeds', 'Fertilizer', 'Labor', 'Equipment', 'Transport', 'Others']
        cost_breakdown = {}
        total_investment = 0.0

        for etype in expense_types:
            amount = Expense.objects.filter(
                user=user,
                crop=crop.crop_name,  # ✅ crop is CharField
                expense_type__iexact=etype
            ).aggregate(total=Sum('paying_amount'))['total'] or 0
            amount = round(float(amount), 2)
            cost_breakdown[etype] = amount
            total_investment += amount

        # 💰 Revenue: QuickSale
        quick_sale_total = QuickSale.objects.filter(
            user=user,
            crop_name__iexact=crop.crop_name  # ✅ crop_name is CharField
        ).aggregate(total=Sum('amount'))['total'] or 0
        quick_sale_total = round(float(quick_sale_total), 2)

        # 📦 Revenue: DetailedSale
        detailed_sale_total = 0.0
        detailed_sales = DetailedSale.objects.filter(user=user)
        for sale in detailed_sales:
            for item in sale.crops:
                if item.get("crop_name", "").strip().lower() == crop_name_key:
                    detailed_sale_total += float(item.get("total_amount", 0))
        detailed_sale_total = round(detailed_sale_total, 2)

        revenue_sources = {
            "Quick Sale": quick_sale_total,
            "Detailed Sale": detailed_sale_total
        }

        # 📊 Financial Summary
        total_revenue = quick_sale_total + detailed_sale_total
        profit = round(total_revenue - total_investment, 2)
        roi_percent = round((profit / total_investment) * 100, 2) if total_investment > 0 else 0.0

        return Response({
            "crop_name": crop.crop_name,
            "field_name": crop.field_name,
            "field_size": f"{crop.field_size} {crop.field_unit}",
            "crop_type": crop.crop_type,
            "sowing_date": crop.sowing_date,
            "irrigation_source": crop.irrigation_source,
            "investment": round(total_investment, 2),
            "revenue": round(total_revenue, 2),
            "profit": profit,
            "roi_percent": roi_percent,
            "cost_breakdown": cost_breakdown,
            "revenue_sources": revenue_sources
        })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPaidMember
from sale.models import QuickSale, DetailedSale
from expenses.models import Expense
from django.db.models import Sum
from crop.models import Crop
from datetime import datetime
from calendar import monthrange

class MonthlyTrendsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        year = int(request.query_params.get('year', datetime.today().year))

        months = []
        revenue_data = []
        expense_data = []
        profit_data = []

        for month in range(1, 13):
            month_name = datetime(year, month, 1).strftime('%b')
            months.append(month_name)

            start_date = datetime(year, month, 1).date()
            end_day = monthrange(year, month)[1]
            end_date = datetime(year, month, end_day).date()

            # Revenue
            quick_sale = QuickSale.objects.filter(
                user=user, created_at__date__range=[start_date, end_date]
            ).aggregate(total=Sum('amount'))['total'] or 0

            detailed_sale = DetailedSale.objects.filter(
                user=user, sale_date__range=[start_date, end_date]
            ).aggregate(total=Sum('total_sale_amount'))['total'] or 0

            revenue = quick_sale + detailed_sale

            # Expenses
            expense = Expense.objects.filter(
                user=user, date__range=[start_date, end_date]
            ).aggregate(total=Sum('paying_amount'))['total'] or 0

            profit = revenue - expense

            revenue_data.append(round(revenue, 2))
            expense_data.append(round(expense, 2))
            profit_data.append(round(profit, 2))

        return Response({
            "year": year,
            "months": months,
            "revenue": revenue_data,
            "expenses": expense_data,
            "profit": profit_data
        })




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPaidMember
from sale.models import QuickSale, DetailedSale
# from income.models import Subsidy, OtherIncome
from django.db.models import Sum
from datetime import datetime

class IncomeSourcesAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        month = int(request.query_params.get('month', datetime.today().month))
        year = int(request.query_params.get('year', datetime.today().year))

        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month + 1, 1).date() if month < 12 else datetime(year + 1, 1, 1).date()

        # Product Sale
        quick_sale = QuickSale.objects.filter(
            user=user, created_at__date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

        detailed_sale = DetailedSale.objects.filter(
            user=user, sale_date__range=[start_date, end_date]
        ).aggregate(total=Sum('total_sale_amount'))['total'] or 0

        product_sale = quick_sale + detailed_sale

        # # Subsidy
        # subsidy = Subsidy.objects.filter(
        #     user=user, date__range=[start_date, end_date]
        # ).aggregate(total=Sum('amount'))['total'] or 0

        # # Other Income
        # other_income = OtherIncome.objects.filter(
        #     user=user, date__range=[start_date, end_date]
        # ).aggregate(total=Sum('amount'))['total'] or 0

        return Response([
            { "source": "Product Sale", "amount": round(product_sale, 2) },
            # { "source": "Subsidy", "amount": round(subsidy, 2) },
            # { "source": "Other Income", "amount": round(other_income, 2) }
        ])

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPaidMember
from expenses.models import Expense
from django.db.models import Sum
from datetime import datetime

class ExpenseBreakdownAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPaidMember]

    def get(self, request):
        user = request.user
        month = int(request.query_params.get('month', datetime.today().month))
        year = int(request.query_params.get('year', datetime.today().year))

        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()

        categories = ['Seeds', 'Fertilizer', 'Labor', 'Equipment', 'Transport', 'Others']
        total_expense = 0
        breakdown = []

        for category in categories:
            amount = Expense.objects.filter(
                user=user,
                expense_type =category,
                date__range=[start_date, end_date]
            ).aggregate(total=Sum('paying_amount'))['total'] or 0

            total_expense += amount
            breakdown.append({ "category": category, "amount": round(amount, 2) })

        # Add percentage
        for item in breakdown:
            percent = (item["amount"] / total_expense * 100) if total_expense > 0 else 0
            item["percent"] = round(percent, 2)

        return Response(breakdown)















# from django.template.loader import get_template
# from django.http import HttpResponse
# from xhtml2pdf import pisa
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsPaidMember
# from crop.models import Crop
# from sale.models import QuickSale, DetailedSale
# from expenses.models import Expense
# from income.models import Subsidy, OtherIncome
# from django.db.models import Sum

# class ExportReportPDFAPIView(APIView):
#     permission_classes = [IsAuthenticated, IsPaidMember]

#     def get(self, request):
#         user = request.user

#         # Data aggregation
#         total_expense = Expense.objects.filter(user=user).aggregate(Sum('paying_amount'))['paying_amount'] or 0
#         quick_sale = QuickSale.objects.filter(user=user).aggregate(Sum('amount'))['amount'] or 0
#         detailed_sale = DetailedSale.objects.filter(user=user).aggregate(Sum('total_sale_amount'))['total_sale_amount'] or 0
#         subsidy = Subsidy.objects.filter(user=user).aggregate(Sum('amount'))['amount'] or 0
#         other_income = OtherIncome.objects.filter(user=user).aggregate(Sum('amount'))['amount'] or 0

#         total_revenue = quick_sale + detailed_sale + subsidy + other_income
#         profit = total_revenue - total_expense
#         roi = round((profit / total_expense) * 100, 2) if total_expense > 0 else 0

#         # Crop summaries
#         crops = Crop.objects.filter(user=user)
#         crop_data = []
#         for crop in crops:
#             name = crop.crop_name
#             sale_total = 0
#             detailed_sales = DetailedSale.objects.filter(user=user)
#             for sale in detailed_sales:
#                 for item in sale.crops:
#                     if item.get("crop_name", "").lower() == name.lower():
#                         sale_total += item.get("total_amount", 0)
#             investment = Expense.objects.filter(user=user, crop_name__iexact=name).aggregate(Sum('paying_amount'))['paying_amount'] or 0
#             revenue = quick_sale + sale_total
#             profit = revenue - investment
#             roi = round((profit / investment) * 100, 2) if investment > 0 else 0

#             crop_data.append({
#                 "name": name,
#                 "field": crop.field_name,
#                 "size": f"{crop.field_size} {crop.field_unit}",
#                 "investment": investment,
#                 "revenue": revenue,
#                 "profit": profit,
#                 "roi": roi
#             })

#         # Render PDF
#         template = get_template("report_template.html")
#         html = template.render({
#             "user": user,
#             "total_revenue": total_revenue,
#             "total_expense": total_expense,
#             "profit": profit,
#             "roi": roi,
#             "crop_data": crop_data
#         })

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="AgroGanit_Report.pdf"'
#         pisa_status = pisa.CreatePDF(html, dest=response)

#         return response if not pisa_status.err else HttpResponse("PDF generation failed", status=500)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsPaidMember
# from django.core.mail import EmailMessage
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import os
# import tempfile

# class ShareReportAPIView(APIView):
#     permission_classes = [IsAuthenticated, IsPaidMember]

#     def post(self, request):
#         user = request.user
#         method = request.data.get('method')  # 'email' or 'whatsapp'
#         target = request.data.get('target')  # email ID or phone number

#         if not method or not target:
#             return Response({ "error": "method and target are required" }, status=400)

#         # Generate PDF
#         template = get_template("report_template.html")
#         html = template.render({ "user": user })
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
#         pisa_status = pisa.CreatePDF(html, dest=temp_file)

#         if pisa_status.err:
#             return Response({ "error": "PDF generation failed" }, status=500)

#         # Sharing logic
#         if method == 'email':
#             email = EmailMessage(
#                 subject="Your AgroGanit Report",
#                 body="Please find attached your latest farm financial report.",
#                 to=[target]
#             )
#             email.attach_file(temp_file.name)
#             email.send()
#             response_msg = f"Report sent to {target} via Email"

#         elif method == 'whatsapp':
#             # You’d integrate Twilio or WhatsApp Business API here
#             # For now, just simulate response
#             response_msg = f"Report shared with {target} on WhatsApp (simulation)"

#         else:
#             return Response({ "error": "Unsupported method" }, status=400)

#         # Clean up
#         temp_file.close()
#         os.remove(temp_file.name)

#         return Response({ "success": True, "message": response_msg })
