# Generated by Django 5.0.4 on 2024-04-13 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machineLearning', '0002_dashboard_data_alter_dashboard_forecast'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dashboard',
            options={'verbose_name': 'Дашборд', 'verbose_name_plural': 'Дашборды'},
        ),
        migrations.AddField(
            model_name='dashboard',
            name='adfuler_test',
            field=models.JSONField(blank=True, null=True, verbose_name='Тест на стационарность временного ряда'),
        ),
        migrations.AddField(
            model_name='dashboard',
            name='cointegration_test',
            field=models.JSONField(blank=True, null=True, verbose_name='Коинтеграционный тест'),
        ),
        migrations.AddField(
            model_name='dashboard',
            name='correlation_stat',
            field=models.JSONField(blank=True, null=True, verbose_name='Корреляция'),
        ),
        migrations.AddField(
            model_name='dashboard',
            name='granger_test',
            field=models.JSONField(blank=True, null=True, verbose_name='Тест Грейнжера'),
        ),
    ]
