import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from fv_bb_package.time_series_forecasting import FirstPlace
from machineLearning.models import Dashboard
from machineLearning.serializers import FileSerializer, ForecastSerializer


class GetDatasetAPIView(GenericAPIView):
    parser_classes = [MultiPartParser, FileUploadParser]
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, format=None):
        data = {
            'data': request.FILES['file'],
            'user': request.user.pk,
            "forecast": json.dumps({"predict": "z"}),
            "correlation_stat": json.dumps({"corr": "v"}),
            "granger_test": json.dumps({"granger": "z"}),
            "adfuler_test": json.dumps({"adfuler": "z"}),
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            time_series = FirstPlace(request.FILES['file'])
            time_series.fit_stacking()
            forecast = time_series.get_predict()
            corr_stat = time_series.get_heatmap()
            granger_test = time_series.granger_test()
            adfuler_test = time_series.get_adfuller_test()
            serializer.validated_data['forecast'] = forecast
            serializer.validated_data['correlation_stat'] = corr_stat
            serializer.validated_data['granger_test'] = granger_test
            serializer.validated_data['adfuler_test'] = adfuler_test
            serializer.validated_data['history_value'] = time_series.get_history_value()
            serializer.validated_data['forecast_indexes'] = time_series.get_indexes()
            serializer.save()
            return JsonResponse({**serializer.data}, status=status.HTTP_201_CREATED, safe=False)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetForecastAPIView(GenericAPIView):
    serializer_class = ForecastSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, format=None):
        dashboard_data = Dashboard.objects.get(pk=request.data['pk'])
        serializer = self.serializer_class(dashboard_data)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
