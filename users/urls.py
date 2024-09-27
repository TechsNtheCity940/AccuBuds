from django.urls import path
from .views import password_reset_request
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('password_reset/', password_reset_request, name='password_reset'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # You can add other user-related URLs here, like login, logout, etc.
]
