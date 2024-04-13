import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.request import Request

from machineLearning.models import Dashboard
from machineLearning.serializers import FileSerializer


class GetDatasetAPIView(GenericAPIView):
    parser_classes = [MultiPartParser, FileUploadParser]
    serializer_class = FileSerializer

    def post(self, request: Request, format=None):
        data = {
            'data': request.FILES['file'],
            'user': request.user.pk
        }
        serializer = self.serializer_class(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "OK"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetForecastAPIView(GenericAPIView):
    serializer_class = FileSerializer

    def get(self, request: Request, format=None):
        last_record = Dashboard.objects.filter(user=request.user.pk).last()
        # TODO: make some magic
        data = {
            "user": request.user.pk,
            "forecast": json.dumps({"predict": "сиськи"})
        }
        serializer = self.serializer_class(data=data, many=False)
        if serializer.is_valid():
            last_record.forecast = data['forecast']
            last_record.save()
            return JsonResponse({"status": "OK"}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
