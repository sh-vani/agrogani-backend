# adminauth/urls.py

from django.urls import path
from .views import AdminSignupView, AdminLoginView

urlpatterns = [
    path('signup/', AdminSignupView.as_view(), name='admin-signup'),
    path('login/', AdminLoginView.as_view(), name='admin-login'),
]