from django.urls import path
from .views import SensorListView, SensorDetailView, MeasurementView


urlpatterns = [
    path('sensors/', SensorListView.as_view()),
    path('sensors/<pk>/', SensorDetailView.as_view()),
    path('measurements/', MeasurementView.as_view()),
]