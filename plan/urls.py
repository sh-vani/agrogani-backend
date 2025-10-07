from django.urls import path
from .views import  CreateOrderView, PaymentSuccessView, ActivePlanView
urlpatterns = [
    # path('plans/', PlanListView.as_view()),
    #  path('plans/<int:pk>/', PlanDetailView.as_view(), name='plan-detail'),

    path('create-order/', CreateOrderView.as_view()),
    path('payment-success/', PaymentSuccessView.as_view()),
    path('active-plan/', ActivePlanView.as_view()),
]


# plans/urls.py
from django.urls import path
from .views import (
    AdminPlanListView,
    AdminPlanDetailView,
    UserPlanListView,
    UserPlanDetailView
)

urlpatterns = [
    # Admin URLs (JWT required for CRUD)
    path('admin/plans/', AdminPlanListView.as_view(), name='admin-plan-list-create'),
    path('admin/plans/<int:pk>/', AdminPlanDetailView.as_view(), name='admin-plan-detail'),
    
    # User URLs (JWT required for viewing)
    path('plans/', UserPlanListView.as_view(), name='user-plan-list'),        # ✅ JWT required
    path('plans/<int:pk>/', UserPlanDetailView.as_view(), name='user-plan-detail'), # ✅ JWT required
]