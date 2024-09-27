from django.db import models

class Patient(models.Model):
    patient_name = models.CharField(max_length=255)
    patient_id = models.CharField(max_length=255, unique=True)
    prescription_details = models.TextField()
    medical_card_id = models.CharField(max_length=255, unique=True)
    medical_card_expiration = models.DateField()

    def __str__(self):
        return f"{self.patient_name} - {self.medical_card_id}"
