# Generated by Django 2.0.7 on 2019-09-25 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunya', '0008_auto_20190925_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='health',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]