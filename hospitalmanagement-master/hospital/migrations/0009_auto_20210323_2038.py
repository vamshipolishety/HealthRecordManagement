# Generated by Django 3.1.1 on 2021-03-24 00:38

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0008_auto_20210323_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='prescription',
            field=django_cryptography.fields.encrypt(models.TextField(blank=True, max_length=2000)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='address',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=40)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='department',
            field=django_cryptography.fields.encrypt(models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Dermatologists', 'Dermatologists'), ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'), ('Allergists/Immunologists', 'Allergists/Immunologists'), ('Anesthesiologists', 'Anesthesiologists'), ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')], default='Cardiologist', max_length=50)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='mobile',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=20, null=True)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=40)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='admitDate',
            field=django_cryptography.fields.encrypt(models.DateField(auto_now=True)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='mobile',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=20)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='symptoms',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=100)),
        ),
    ]
