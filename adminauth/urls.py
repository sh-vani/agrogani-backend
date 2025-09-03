# adminauth/urls.py
from django.urls import path
from .views import AdminSignupView

urlpatterns = [
    path('signup/', AdminSignupView.as_view(), name='admin-signup'),
]
