# Generated by Django 2.0.7 on 2019-10-02 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunya', '0013_organization_imei'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='imei',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]