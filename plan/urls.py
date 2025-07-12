from django.urls import path
from .views import PlanListView, CreateOrderView, PaymentSuccessView, ActivePlanView

urlpatterns = [
    path('plans/', PlanListView.as_view()),
    path('create-order/', CreateOrderView.as_view()),
    path('payment-success/', PaymentSuccessView.as_view()),
    path('active-plan/', ActivePlanView.as_view()),
]
