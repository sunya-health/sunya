# Generated by Django 2.0.7 on 2019-09-08 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sunya', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization_user',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunya.Organization', to_field='device_id'),
        ),
    ]