from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from datetime import date, timedelta
from .models import Buyer, Sale
from .serializers import BuyerSerializer, SaleSerializer
from .permissions import IsPaidUser

class BuyerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsPaidUser]
    serializer_class = BuyerSerializer

    def get_queryset(self):
        return Buyer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LedgerSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPaidUser]

    def get(self, request, buyer_id):
        sales = Sale.objects.filter(user=request.user, buyer_id=buyer_id)
        total_sale = sales.aggregate(Sum('total_value'))['total_value__sum'] or 0
        total_received = sales.aggregate(Sum('received_amount'))['received_amount__sum'] or 0
        remaining_due = total_sale - total_received
        last_sale = sales.order_by('-sale_date').first()
        return Response({
            'total_sale': total_sale,
            'total_received': total_received,
            'remaining_due': remaining_due,
            'last_sale_date': last_sale.sale_date if last_sale else None
        })

class SaleListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsPaidUser]
    serializer_class = SaleSerializer

    def get_queryset(self):
        buyer_id = self.kwargs['buyer_id']
        queryset = Sale.objects.filter(user=self.request.user, buyer_id=buyer_id)
        crop = self.request.query_params.get('crop')
        time_filter = self.request.query_params.get('time')

        if crop:
            queryset = queryset.filter(crop=crop)

        if time_filter:
            today = date.today()
            if time_filter == "today":
                queryset = queryset.filter(sale_date=today)
            elif time_filter == "yesterday":
                queryset = queryset.filter(sale_date=today - timedelta(days=1))
            elif time_filter == "week":
                start_week = today - timedelta(days=today.weekday())
                queryset = queryset.filter(sale_date__gte=start_week)
            # You can add 'month' and 'range' logic here

        return queryset
