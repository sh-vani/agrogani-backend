from django.urls import path
from .views import ShopCreateView, ShopListView,BuyerAddView
# BuyerListViewgvfc
urlpatterns = [
    path('add/', ShopCreateView.as_view(), name='add-shop'),
    path('list/', ShopListView.as_view(), name='shop-list'),
    path('buyer/add/', BuyerAddView.as_view(), name='buyer-add'),
    # path('buyer/list/', BuyerListView.as_view(), name='buyer-list'),


]
