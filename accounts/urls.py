from django.urls import path
from .views import RegisterView, VerifyOTPView, SetPasswordView
from .views import LoginView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('set-password/', SetPasswordView.as_view()),
     path('login/', LoginView.as_view()),
]



