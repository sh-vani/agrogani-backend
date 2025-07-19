from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseCreateView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Expense
from shop.models import Shop
from crop.models import Crop  # only if crop filtering needed
from .permission import IsPaidUserPlan
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated

class ShopLedgerView(APIView):
    permission_classes = [IsAuthenticated, IsPaidUserPlan]

    def get(self, request, shop_id):
        user = request.user
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        expense_type = request.GET.get("expense_type")
        crop_id = request.GET.get("crop_id")

        try:
            shop = Shop.objects.get(id=shop_id, user=user)
        except Shop.DoesNotExist:
            return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)

        queryset = Expense.objects.filter(user=user, shop=shop)

        # Apply filters
        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)
        if expense_type:
            queryset = queryset.filter(expense_type=expense_type)
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)

        total_amount = queryset.aggregate(Sum('paying_amount'))['paying_amount__sum'] or 0
        total_paid = queryset.filter(payment_type='cash').aggregate(Sum('paying_amount'))['paying_amount__sum'] or 0
        total_due = total_amount - total_paid

        bills = []
        for exp in queryset.order_by('-date'):
            bills.append({
                "bill_no": exp.bill_no,
                "date": exp.date,
                "crop": exp.crop.name if exp.crop else None,
                "expense_type": exp.expense_type,
                "total_amount": exp.paying_amount,
                "paid_amount": exp.paying_amount if exp.payment_type == 'cash' else 0,
                "due_amount": exp.paying_amount if exp.payment_type == 'credit' else 0,
                "status": "Paid" if exp.payment_type == 'cash' else ("Due" if exp.paying_amount else "Partial Paid")
            })

        latest_transaction = queryset.order_by('-date').first()

        return Response({
            "shop": shop.name,
            "total_amount": total_amount,
            "total_paid": total_paid,
            "total_due": total_due,
            "last_transaction": latest_transaction.date if latest_transaction else None,
            "bills": bills
        })






import pandas as pd
from django.http import HttpResponse
from io import BytesIO
from .models import Expense
from shop.models import Shop
from .permission import IsPaidUserPlan
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from datetime import datetime

class ShopLedgerExcelExport(APIView):
    permission_classes = [IsAuthenticated, IsPaidUserPlan]

    def get(self, request, shop_id):
        user = request.user
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        expense_type = request.GET.get("expense_type")
        crop_id = request.GET.get("crop_id")

        try:
            shop = Shop.objects.get(id=shop_id, user=user)
        except Shop.DoesNotExist:
            return HttpResponse("Shop not found", status=404)

        queryset = Expense.objects.filter(user=user, shop=shop)

        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)
        if expense_type:
            queryset = queryset.filter(expense_type=expense_type)
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)

        data = []
        total_amount = 0
        total_paid = 0
        total_due = 0

        for exp in queryset.order_by('-date'):
            paid = exp.paying_amount if exp.payment_type == 'cash' else 0
            due = exp.paying_amount if exp.payment_type == 'credit' else 0
            total_amount += exp.paying_amount
            total_paid += paid
            total_due += due

            data.append({
                "Bill No": exp.bill_no,
                "Date": exp.date.strftime("%Y-%m-%d"),
                "Crop": exp.crop.name if exp.crop else '',
                "Expense Type": exp.expense_type,
                "Amount": float(exp.paying_amount),
                "Paid": float(paid),
                "Due": float(due),
                "Status": "Paid" if exp.payment_type == 'cash' else ("Due" if due else "Partial Paid"),
            })

        df = pd.DataFrame(data)

        # Add summary row
        df.loc[len(df.index)] = ['Total', '', '', '', total_amount, total_paid, total_due, '']

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Shop Ledger')
        writer.save()
        output.seek(0)

        filename = f"Shop_Ledger_{shop.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response




class ShopLedgerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, shop_id):
        user = request.user
        try:
            shop = Shop.objects.get(id=shop_id, user=user)
        except Shop.DoesNotExist:
            return Response({"error": "Shop not found."}, status=404)

        expenses = Expense.objects.filter(user=user, shop=shop)

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        expense_type = request.GET.get("expense_type")
        crop_id = request.GET.get("crop_id")

        if from_date:
            expenses = expenses.filter(date__gte=from_date)
        if to_date:
            expenses = expenses.filter(date__lte=to_date)
        if expense_type:
            expenses = expenses.filter(expense_type=expense_type)
        if crop_id:
            expenses = expenses.filter(crop_id=crop_id)

        total_amount = sum(e.paying_amount for e in expenses)
        total_paid = sum(e.paid_amount for e in expenses)
        total_due = total_amount - total_paid
        last_transaction = expenses.order_by("-date").first().date if expenses.exists() else None

        bills = []
        for exp in expenses.order_by("-date"):
            status = "Paid" if exp.paid_amount == exp.paying_amount else ("Partial Paid" if exp.paid_amount > 0 else "Due")
            bills.append({
                "bill_no": exp.bill_no,
                "date": exp.date,
                "crop": exp.crop.name,
                "expense_type": exp.expense_type,
                "total_amount": exp.paying_amount,
                "paid_amount": exp.paid_amount,
                "due_amount": exp.paying_amount - exp.paid_amount,
                "status": status
            })

        return Response({
            "shop": shop.name,
            "total_amount": total_amount,
            "total_paid": total_paid,
            "total_due": total_due,
            "last_transaction": last_transaction,
            "bills": bills
        })
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Expense  # make sure Expense model is imported

class AllShopLedgerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        expenses = Expense.objects.filter(user=user)

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        expense_type = request.GET.get("expense_type")
        crop_id = request.GET.get("crop_id")

        if from_date:
            expenses = expenses.filter(date__gte=from_date)
        if to_date:
            expenses = expenses.filter(date__lte=to_date)
        if expense_type:
            expenses = expenses.filter(expense_type=expense_type)
        if crop_id:
            expenses = expenses.filter(crop_id=crop_id)

        total_amount = sum(e.paying_amount for e in expenses)
        total_paid = sum(e.paid_amount for e in expenses)
        total_due = total_amount - total_paid
        last_transaction = expenses.order_by("-date").first().date if expenses.exists() else None

        bills = []
        for exp in expenses.order_by("-date"):
            status = "Paid" if exp.paid_amount == exp.paying_amount else ("Partial Paid" if exp.paid_amount > 0 else "Due")
            bills.append({
                "bill_no": exp.bill_no,
                "date": exp.date,
                "shop": exp.shop.name if exp.shop else None,
                "crop": exp.crop.name,
                "expense_type": exp.expense_type,
                "total_amount": exp.paying_amount,
                "paid_amount": exp.paid_amount,
                "due_amount": exp.paying_amount - exp.paid_amount,
                "status": status
            })

        return Response({
            "shop": "All Shops",
            "total_amount": total_amount,
            "total_paid": total_paid,
            "total_due": total_due,
            "last_transaction": last_transaction,
            "bills": bills
        })



from rest_framework import generics, permissions, filters
from .models import Expense
from .serializers import ExpenseSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ExpenseListAPIView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['expense_type', 'date', 'crop', 'shop']
    ordering_fields = ['date', 'paying_amount']
    ordering = ['-date']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Expense
from django.db.models import Sum

class AllShopLedgerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        expenses = Expense.objects.filter(user=user)

        # Filters
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        expense_type = request.GET.get("expense_type")

        if from_date:
            expenses = expenses.filter(date__gte=from_date)
        if to_date:
            expenses = expenses.filter(date__lte=to_date)
        if expense_type:
            expenses = expenses.filter(expense_type=expense_type)

        total_amount = expenses.aggregate(Sum('paying_amount'))['paying_amount__sum'] or 0
        total_paid = sum(exp.paying_amount if exp.payment_type == 'cash' else 0 for exp in expenses)
        total_due = total_amount - total_paid

        bills = []
        for exp in expenses.order_by('-date'):
            paid = exp.paying_amount if exp.payment_type == 'cash' else 0
            due = exp.paying_amount if exp.payment_type == 'credit' else 0
            status = "Paid" if paid == exp.paying_amount else ("Partial Paid" if paid > 0 else "Due")

            bills.append({
                "bill_no": exp.bill_no,
                "date": exp.date,
                # "shop": exp.shop.name if exp.shop else None,
                # "crop": exp.crop,
                # "expense_type": exp.expense_type,
                "total_amount": exp.paying_amount,
                "paid_amount": paid,
                "due_amount": due,
                "status": status
            })

        latest_transaction = expenses.order_by('-date').first()

        return Response({
            "shop": "All Shops",
            "total_amount": total_amount,
            "total_paid": total_paid,
            "total_due": total_due,
            "last_transaction": latest_transaction.date if latest_transaction else None,
            "bills": bills
        })





from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Expense

class OverallLedgerSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)

    
        summary = {
    "total_amount": expenses.aggregate(Sum('paying_amount'))['paying_amount__sum'] or 0,
    "total_paid": expenses.aggregate(Sum('paying_amount'))['paying_amount__sum'] or 0,
    "total_due": 0,  # agar due_amount naam ka field nahi hai to calculate manually
    "last_transaction": expenses.latest('date').date.strftime("%d %B %Y") if expenses.exists() else "N/A"
}


        return Response(summary)


from .models import Expense

class FullTransactionHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user).select_related('shop').order_by('-date')

        transactions = []
        for exp in expenses:
            transactions.append({
                "bill_id": f"{exp.date.strftime('%Y%m%d')}{exp.id}",
                "shop_name": exp.shop.name if exp.shop else "N/A",
                "date": exp.date.strftime("%d %B %Y"),
                "amount": float(exp.paying_amount),

                "paid": float(exp.paid_amount),
                "due": float(exp.due_amount),
                "status": "Paid" if exp.due_amount == 0 else "Partial Paid" if exp.paid_amount > 0 else "Unpaid"
            })

        return Response(transactions)
