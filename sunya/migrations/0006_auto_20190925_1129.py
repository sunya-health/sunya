# Generated by Django 2.0.7 on 2019-09-25 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunya', '0005_auto_20190925_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='health',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
