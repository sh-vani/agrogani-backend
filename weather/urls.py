from django.urls import path
from .views import TodayWeatherView

urlpatterns = [
    path('api/weather/today/', TodayWeatherView.as_view(), name='today-weather')
]
