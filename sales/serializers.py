# sales/serializers.py

from rest_framework import serializers
from .models import Sale

class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sale model.
    """
    class Meta:
        model = Sale
        fields = '__all__'
