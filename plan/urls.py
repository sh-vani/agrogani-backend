from django.urls import path
from .views import PlanListView, CreateOrderView, PaymentSuccessView, ActivePlanView,PlanDetailView

urlpatterns = [
    path('plans/', PlanListView.as_view()),
     path('plans/<int:pk>/', PlanDetailView.as_view(), name='plan-detail'),

    path('create-order/', CreateOrderView.as_view()),
    path('payment-success/', PaymentSuccessView.as_view()),
    path('active-plan/', ActivePlanView.as_view()),
]
