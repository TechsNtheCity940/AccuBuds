from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from patients.views import PatientViewSet
from inventory.views import ProductViewSet
from sales.views import SaleViewSet
from users.views import UserViewSet, login_with_pin, logout

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', login_with_pin, name='login-with-pin'),
    path('api/logout/', logout, name='logout'),
    path('api/token/', obtain_auth_token, name='api-token'),
]
