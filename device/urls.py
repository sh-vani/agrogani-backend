from django.urls import path
from .views import DeviceLoginView

urlpatterns = [
    path("device-login/", DeviceLoginView.as_view(), name="device-login"),
]
