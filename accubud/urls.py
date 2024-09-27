from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from patients.views import PatientViewSet
from inventory.views import ProductViewSet
from sales.views import SaleViewSet
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/')),  # Redirect root to admin panel
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
