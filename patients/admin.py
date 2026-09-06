from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient_id', 'medical_card_id', 'medical_card_expiration')
    search_fields = ('patient_name', 'patient_id', 'medical_card_id')
