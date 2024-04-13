import os
from typing import Dict

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from machineLearning.models import Dashboard


class FileSerializer(serializers.ModelSerializer):
    # file = serializers.FileField()
    class Meta:
        model = Dashboard
        fields = '__all__'


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ('user', 'forecast')
