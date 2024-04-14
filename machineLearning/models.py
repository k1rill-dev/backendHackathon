from django.db import models
from django.db.models import JSONField

from authentication.models import User


class Dashboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Пользователь", verbose_name="Пользователь")
    data = models.FileField(upload_to='media/tmp', verbose_name="Данные", default=None)
    forecast = JSONField(verbose_name="Предсказания", null=True, blank=True)
    forecast_indexes = JSONField(verbose_name="Даты, по которым шел прогноз", null=True, blank=True)
    correlation_stat = JSONField(verbose_name="Корреляция", null=True, blank=True)
    granger_test = JSONField(verbose_name="Тест Грейнжера", null=True, blank=True)
    adfuler_test = JSONField(verbose_name="Тест на стационарность временного ряда", null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Дашборд"
        verbose_name_plural = "Дашборды"
