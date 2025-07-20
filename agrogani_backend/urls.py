"""
URL configuration for agrogani_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def health_check(request):
    return JsonResponse({'status': 'Backend live 🚀'})

urlpatterns = [
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('', health_check),

    path('admin/', admin.site.urls),
    path('api/account/', include('accounts.urls')),
    path('api/userprofile/', include('userprofile.urls')),
    path('api/plan/', include('plan.urls')),
    path("api/device/", include("device.urls")),
    # path('api/weather/', include('weather.urls')),
    path('api/crop/', include('crop.urls')),
     path('api/labour/', include('labour.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/shop/', include('shop.urls')),
     path('api/reports/', include('reports.urls')),
 

    path('api/sale/', include('sale.urls')),
    #  path('api/shop_ledger/',include('shop_ledger.urls')),
    path('api/Task/',include('task.urls')),
    # path('api/advisory/',include('advisory.urls')),
] 



from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

