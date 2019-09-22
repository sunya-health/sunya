from django.db import models
from account.models import User
# Create your models here.


class Organization(models.Model):
    device_id = models.CharField(max_length=150, unique=True)
    address = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    urine_strip = models.IntegerField(default=0)
    blood_strip = models.IntegerField(default=0)


class Organization_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Organization, on_delete=models.CASCADE, to_field='device_id')


class Clients(models.Model):
    user_id = models.CharField(max_length=255, unique=True)

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)

    device = models.ForeignKey(Organization, on_delete=models.CASCADE, to_field='device_id')


class Vital_sign(models.Model):
    user = models.ForeignKey(Clients, on_delete=models.CASCADE, to_field='user_id')
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    pulse = models.FloatField(blank=True, null=True)
    bp_systolic = models.FloatField(blank=True, null=True)
    bp_diastolic = models.FloatField(blank=True, null=True)
    sto2 = models.FloatField(blank=True, null=True)


class Blood_test(models.Model):
    user = models.ForeignKey(Clients, on_delete=models.CASCADE, to_field='user_id')
    glucose = models.FloatField(blank=True, null=True)
    cholesterol = models.FloatField(blank=True, null=True)
    uric_acid = models.FloatField(blank=True, null=True)


class Urine_test(models.Model):
    user = models.ForeignKey(Clients, on_delete=models.CASCADE, to_field='user_id')
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
    user = models.ForeignKey(Clients, on_delete=models.CASCADE, to_field='user_id')
    device = models.ForeignKey(Organization, on_delete=models.CASCADE, to_field='device_id')
    vital_sign = models.ForeignKey(Vital_sign, on_delete=models.CASCADE, blank=True, null=True)
    blood_test = models.ForeignKey(Blood_test, on_delete=models.CASCADE, blank=True, null=True)
    urine_test = models.ForeignKey(Urine_test, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField()







