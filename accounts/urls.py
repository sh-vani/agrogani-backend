from django.urls import path
from .views import RegisterView, VerifyOTPView, SetPasswordView,CreatePlanOrderAPIView, VerifyPaymentAPIView,dashboard_header,FarmersListView,FarmerDetailView
from .views import (LoginView,WeatherAPIView,ForgotPasswordRequestView,ForgotPasswordVerifyOTPView,ResetPasswordView,RecentActivityAPI,ChangePasswordView, DashboardSummaryAPIView)
# recent_user_activities

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('set-password/', SetPasswordView.as_view()),
    path('login/', LoginView.as_view()),
        
    path('forgot-password/', ForgotPasswordRequestView.as_view(), name='forgot-password'),
    path('forgot/verify-otp/', ForgotPasswordVerifyOTPView.as_view(), name='forgot-password-verify-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

# razorpay path
    path('create-plan-order/', CreatePlanOrderAPIView.as_view(), name='create-plan-order'),
    path('verify-payment/', VerifyPaymentAPIView.as_view(), name='verify-payment'),


# dhashboar welcome
     path('header/', dashboard_header, name='dashboard-header'),
     path("weather/", WeatherAPIView.as_view(), name="weather-api"),

    



    path('recent-activities/', RecentActivityAPI.as_view(), name='recent_activities'),

 path("admin/dhasboard/", DashboardSummaryAPIView.as_view(), name="dhasboard-summary"),
 
    
    path('farmers/', FarmersListView.as_view(), name='farmers-list'),
    path('farmers/<int:pk>/', FarmerDetailView.as_view(), name='farmer-detail'),

]



