# Generated by Django 3.1.1 on 2021-03-23 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_auto_20210322_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='prescription',
            field=models.TextField(blank=True, max_length=2000),
        ),
    ]
