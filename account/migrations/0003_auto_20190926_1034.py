# Generated by Django 2.0.7 on 2019-09-26 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_is_orguser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
