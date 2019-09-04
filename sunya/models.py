from django.db import models
from account.models import User
# Create your models here.


class Vital_sign(models.Model):
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    pulse = models.FloatField(blank=True, null=True)
    bp_systolic = models.FloatField(blank=True, null=True)
    bp_diastolic = models.FloatField(blank=True, null=True)
    sto2 = models.FloatField(blank=True, null=True)


class Blood_test(models.Model):
    glucose = models.FloatField(blank=True, null=True)
    cholesterol = models.FloatField(blank=True, null=True)
    uric_acid = models.FloatField(blank=True, null=True)


class Urine_test(models.Model):
    leukocytes = models.FloatField(blank=True, null=True)
    nitrate = models.FloatField(blank=True, null=True)
    urobilinogen = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    blood = models.FloatField(blank=True, null=True)
    sp_gravity = models.FloatField(blank=True, null=True)
    ketone = models.FloatField(blank=True, null=True)
    bilirubin = models.FloatField(blank=True, null=True)
    glucose = models.FloatField(blank=True, null=True)
    ascorbic_acid = models.FloatField(blank=True, null=True)


class Health(models.Model):
    device_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vital_sign = models.ForeignKey(Vital_sign, on_delete=models.CASCADE, blank=True, null=True)
    blood_test = models.ForeignKey(Blood_test, on_delete=models.CASCADE, blank=True, null=True)
    urine_test = models.ForeignKey(Urine_test, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField()





