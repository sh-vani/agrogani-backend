


# advisory/urls.py
from django.urls import path
from .views import (
    # User APIs (logged-in users can view only)
    UserAdvisoryListView,
    UserFertilizerShopListView,
    
    # Admin APIs (JWT required for CRUD)
    AdminAdvisoryListCreateView,
    AdminAdvisoryDetailView,
    AdminFertilizerShopListCreateView,
    AdminFertilizerShopDetailView,
    
    # Dashboard
    AdvisoryShopCountView
)

urlpatterns = [
    # User APIs - Must be logged in (any user can view)
    path('advisories/list/', UserAdvisoryListView.as_view(), name='user-advisory-list'),
    path('shops/list/', UserFertilizerShopListView.as_view(), name='user-shop-list'),
    
    # Admin APIs - Authentication required
    path('admin/advisories/', AdminAdvisoryListCreateView.as_view(), name='admin-advisory-list-create'),
    path('admin/advisories/<int:pk>/', AdminAdvisoryDetailView.as_view(), name='admin-advisory-detail'),
    path('admin/shops/', AdminFertilizerShopListCreateView.as_view(), name='admin-shop-list-create'),
    path('admin/shops/<int:pk>/', AdminFertilizerShopDetailView.as_view(), name='admin-shop-detail'),
    
    # Dashboard count
    path('advisory-count/', AdvisoryShopCountView.as_view(), name='advisory-shop-count'),
]

