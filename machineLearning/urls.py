from django.urls import path

from machineLearning import views

urlpatterns = [
    path('upload', views.GetDatasetAPIView.as_view(), name='GetDatasetAPIView'),
    path('forecast', views.GetForecastAPIView.as_view(), name='GetForecastAPIView'),
]