# Generated by Django 5.0.4 on 2024-04-14 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machineLearning', '0004_remove_dashboard_cointegration_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='forecast_indexes',
            field=models.JSONField(blank=True, null=True, verbose_name='Даты, по которым шел прогноз'),
        ),
    ]
