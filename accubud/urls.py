from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from patients.views import PatientViewSet
from sales.views import SalesViewSet
from users.views import UsersViewSet
from inventory.views import ProductViewSet
from users.views import password_reset_request

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URLs
    path('api/', include(router.urls)),  # API-related URLs
    path('accounts/', include('users.urls')),  # Users app URLs
    path('password_reset/', password_reset_request, name='password_reset'),  # Password reset
    path('sales/', include('sales.urls')),  # Include the sales app URLs
]