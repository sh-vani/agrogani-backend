

from django.urls import path
from .views import (
    QuickSaleAddView,
    QuickSaleListView,
    DetailedSaleAddView,
    DetailedSaleListView,
    CropBuyerLedgerAPIView,
    BuyerLedgerListAPIView,
BuyerLedgerLatestAPIView,

BuyerLedgerTodayAPIView,
CommodityTransactionSummaryAPIView,
    BuyerLedgerMonthlyAPIView,
    BuyerLedgerSummaryAPIView,
       BuyerLedgerDailyAPIView
)

urlpatterns = [
    # 🔹 Quick Sale
    path('quick-sale/add/', QuickSaleAddView.as_view(), name='quick-sale-add'),
    path('quick-sale/view/', QuickSaleListView.as_view(), name='quick-sale-view'),
    # 🔹 Detailed Sale
    path('detailed-sale/add/', DetailedSaleAddView.as_view(), name='detailed-sale-add'),
    path('detailed-sale/view/', DetailedSaleListView.as_view(), name='detailed-sale-view'),
    # 🔹 Crop Buyer Ledger (Single Buyer)
    path('ledger/buyer/<str:buyer_name>/', CropBuyerLedgerAPIView.as_view(), name='buyer-ledger'),

    # 🔹 Buyer Ledger List (All Buyers)
    path('ledger/buyers/', BuyerLedgerListAPIView.as_view(), name='buyer-ledger-list'),

path('buyer-ledger-monthly/', BuyerLedgerMonthlyAPIView.as_view(), name='buyer-ledger-monthly'),
path('buyer-ledger-latest/', BuyerLedgerLatestAPIView.as_view(), name='buyer-ledger-latest'),

      
    path('buyer-ledger-daily/', BuyerLedgerDailyAPIView.as_view(), name='buyer-ledger-daily'),



    
     path('buyer-ledger/', BuyerLedgerTodayAPIView.as_view(), name='buyer-ledger'),


        path('ledger/summary/', BuyerLedgerSummaryAPIView.as_view(), name='buyer-ledger-summary'),
       path('ledger/transaction/',CommodityTransactionSummaryAPIView.as_view(), name='transaction-list'),



]



from .views import CropChartDataAPIView

urlpatterns += [
    path('ledger/crops/chart/', CropChartDataAPIView.as_view(), name='crop-chart-data'),
]

