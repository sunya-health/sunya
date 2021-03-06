# Generated by Django 2.0.7 on 2019-09-08 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_user_is_orguser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blood_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('glucose', models.FloatField(blank=True, null=True)),
                ('cholesterol', models.FloatField(blank=True, null=True)),
                ('uric_acid', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=20, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('blood_test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sunya.Blood_test')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=150, unique=True)),
                ('address', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Organization_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunya.Organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User')),
            ],
        ),
        migrations.CreateModel(
            name='Urine_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leukocytes', models.FloatField(blank=True, null=True)),
                ('nitrate', models.FloatField(blank=True, null=True)),
                ('urobilinogen', models.FloatField(blank=True, null=True)),
                ('protein', models.FloatField(blank=True, null=True)),
                ('ph', models.FloatField(blank=True, null=True)),
                ('blood', models.FloatField(blank=True, null=True)),
                ('sp_gravity', models.FloatField(blank=True, null=True)),
                ('ketone', models.FloatField(blank=True, null=True)),
                ('bilirubin', models.FloatField(blank=True, null=True)),
                ('glucose', models.FloatField(blank=True, null=True)),
                ('ascorbic_acid', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunya.Clients', to_field='user_id')),
            ],
        ),
        migrations.CreateModel(
            name='Vital_sign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('pulse', models.FloatField(blank=True, null=True)),
                ('bp_systolic', models.FloatField(blank=True, null=True)),
                ('bp_diastolic', models.FloatField(blank=True, null=True)),
                ('sto2', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunya.Clients', to_field='user_id')),
            ],
        ),
        migrations.AddField(
            model_name='health',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunya.Organization', to_field='device_id'),
        ),
        migrations.AddField(
            model_name='health',
            name='urine_test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sunya.Urine_test'),
        ),
        migrations.AddField(
            model_name='health',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunya.Clients', to_field='user_id'),
        ),
        migrations.AddField(
            model_name='health',
            name='vital_sign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sunya.Vital_sign'),
        ),
        migrations.AddField(
            model_name='clients',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunya.Organization', to_field='device_id'),
        ),
        migrations.AddField(
            model_name='blood_test',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunya.Clients', to_field='user_id'),
        ),
    ]
