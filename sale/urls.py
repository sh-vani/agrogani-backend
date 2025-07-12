from django.urls import path
from .views import (
    QuickSaleAddView, QuickSaleListView,
    DetailedSaleAddView, DetailedSaleListView
)

urlpatterns = [
    path('quick-sale/add/', QuickSaleAddView.as_view(), name='quick-sale-add'),
    path('quick-sale/view/', QuickSaleListView.as_view(), name='quick-sale-view'),
    path('detailed-sale/add/', DetailedSaleAddView.as_view(), name='detailed-sale-add'),
    path('detailed-sale/view/', DetailedSaleListView.as_view(), name='detailed-sale-view'),
]
