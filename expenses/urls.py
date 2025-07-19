from django.urls import path
from .views import ExpenseCreateView,ShopLedgerView,ShopLedgerExcelExport,AllShopLedgerAPIView,ExpenseListAPIView


urlpatterns = [
    path('add/', ExpenseCreateView.as_view(), name='add-expense'),
     path('list/', ExpenseListAPIView.as_view(), name='list-expense'),
    path('ledger/<int:shop_id>/', ShopLedgerView.as_view(), name='shop-ledger'),
    path('ledger/<int:shop_id>/download/', ShopLedgerExcelExport.as_view(), name='ledger-download'),
   path('expenses/ledger/all/', AllShopLedgerAPIView.as_view(), name='all-expense-ledger'),


]


from django.urls import path
from .views import OverallLedgerSummaryAPIView, FullTransactionHistoryAPIView

urlpatterns = [
    path('shop/ledger/summary/', OverallLedgerSummaryAPIView.as_view(), name='ledger-summary'),
    path('shop/ledger/history/', FullTransactionHistoryAPIView.as_view(), name='ledger-history'),
]

