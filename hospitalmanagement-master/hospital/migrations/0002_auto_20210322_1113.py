# Generated by Django 3.1.1 on 2021-03-22 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
