from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'login_pin', 'is_staff')
    list_filter = UserAdmin.list_filter + ('is_active',)
    fieldsets = UserAdmin.fieldsets + (
        ('AccuBuds info', {'fields': ('phone_number', 'address', 'login_pin')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('AccuBuds info', {'fields': ('phone_number', 'address', 'login_pin')}),
    )
