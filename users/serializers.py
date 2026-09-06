from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'address', 'login_pin',
                  'first_name', 'last_name', 'is_active', 'is_staff')
        read_only_fields = ('id', 'is_staff')
