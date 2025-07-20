from django.urls import path
from .views import RegisterView, VerifyOTPView, SetPasswordView,CreatePlanOrderAPIView, VerifyPaymentAPIView,dashboard_header
from .views import LoginView,WeatherAPIView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('set-password/', SetPasswordView.as_view()),
     path('login/', LoginView.as_view()),
        
# razorpay path
    path('create-plan-order/', CreatePlanOrderAPIView.as_view(), name='create-plan-order'),
    path('verify-payment/', VerifyPaymentAPIView.as_view(), name='verify-payment'),


# dhashboar welcome
path('header/', dashboard_header, name='dashboard-header'),

path("weather/", WeatherAPIView.as_view(), name="weather-api")
]
