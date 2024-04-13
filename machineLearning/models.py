from django.db import models
from django.db.models import JSONField

from authentication.models import User


class Dashboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Пользователь", verbose_name="Пользователь")
    data = models.FileField(upload_to='media/tmp', verbose_name="Данные", default=None)
    forecast = JSONField(verbose_name="Предсказания", null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Предсказания для дашборда"
