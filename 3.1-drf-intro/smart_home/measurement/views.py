from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer


class SensorListView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

 
    def post(self, request):
        sensor = Sensor()
        sensor.name = request.data.get('name')
        sensor.description = request.data.get('description')
        sensor.save()
        return Response({
            'message': f'sensor "{sensor.name}" created'
        })


class SensorDetailView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementView(CreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = MeasurementSerializer