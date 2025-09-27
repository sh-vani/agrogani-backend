from django.urls import path
from .views import AdminSignupView, AdminLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", AdminSignupView.as_view(), name="admin-signup"),
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
