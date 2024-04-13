# Generated by Django 5.0.3 on 2024-03-14 11:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userphoto',
            name='photo',
            field=models.ImageField(null=True, upload_to='avatar/<django.db.models.fields.related.ForeignKey>', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='userphoto',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
