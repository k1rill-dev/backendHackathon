# Generated by Django 5.0.4 on 2024-04-14 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machineLearning', '0005_dashboard_forecast_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='history_value',
            field=models.JSONField(blank=True, null=True, verbose_name='Историческое значение'),
        ),
    ]