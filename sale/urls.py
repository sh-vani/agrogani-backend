

from django.urls import path
from .views import (
    QuickSaleAddView,
    QuickSaleListView,
    DetailedSaleAddView,
    DetailedSaleListView,
    CropBuyerLedgerAPIView,
    BuyerLedgerListAPIView,
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


       path('ledger/summary/', BuyerLedgerSummaryAPIView.as_view(), name='buyer-ledger-summary'),
  

    path('buyer-ledger-daily/', BuyerLedgerDailyAPIView.as_view(), name='buyer-ledger-daily'),


]



from .views import CropChartDataAPIView

urlpatterns += [
    path('ledger/crops/chart/', CropChartDataAPIView.as_view(), name='crop-chart-data'),
]

