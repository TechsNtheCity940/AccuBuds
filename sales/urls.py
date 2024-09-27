from django.urls import path
from .views import process_sale

urlpatterns = [
    path('process/', process_sale, name='process_sale'),
]
