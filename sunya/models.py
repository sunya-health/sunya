from django.db import models
from account.models import User
# Create your models here.


class Vital_sign(models.Model):
    weight = models.FloatField(blank=True)
    height = models.FloatField(blank=True)
    temperature = models.FloatField(blank=True)
    pulse = models.FloatField(blank=True)
    bp_systolic = models.FloatField(blank=True)
    bp_diastolic = models.FloatField(blank=True)
    sto2 = models.FloatField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField()


class blood_test(models.Model):
    glucose = models.FloatField(blank=True)
    cholesterol = models.FloatField(blank=True)
    uric_acid = models.FloatField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField()


class urine_test(models.Model):
    leukocytes = models.FloatField(blank=True)
    nitrate = models.FloatField(blank=True)
    urobilinogen = models.FloatField(blank=True)
    protein = models.FloatField(blank=True)
    ph = models.FloatField(blank=True)
    blood = models.FloatField(blank=True)
    sp_gravity = models.FloatField(blank=True)
    ketone = models.FloatField(blank=True)
    bilirubin = models.FloatField(blank=True)
    glucose = models.FloatField(blank=True)
    ascorbic_acid = models.FloatField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField()




