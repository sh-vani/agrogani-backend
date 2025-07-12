from django.urls import path
from .views import ShopCreateView, ShopListView

urlpatterns = [
    path('add/', ShopCreateView.as_view(), name='add-shop'),
    path('list/', ShopListView.as_view(), name='shop-list'),
]
