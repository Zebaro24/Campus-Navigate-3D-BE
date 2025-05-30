from datetime import datetime, timezone

from django.http import Http404, FileResponse
from django.utils.http import http_date
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from .models import FlightLocation, UniversityModel
from .serializers import FlightLocationSerializer, FlightLocationListSerializer


class FlightLocationListAPIView(ListAPIView):
    queryset = FlightLocation.objects.all()
    serializer_class = FlightLocationListSerializer


class FlightLocationDetailAPIView(RetrieveAPIView):
    queryset = FlightLocation.objects.all()
    serializer_class = FlightLocationSerializer

class ActiveUniversityModelFileView(APIView):
    def get(self, request):
        model = UniversityModel.objects.filter(is_active=True).first()
        if not model or not model.model_file:
            raise Http404("Active model not found")

        file_handle = model.model_file.open()
        response = FileResponse(file_handle, content_type='model/gltf-binary')

        # Отдаём файл под одним именем, чтоб браузер не парился
        response['Content-Disposition'] = 'inline; filename="university_model.glb"'

        # Добавим заголовки для кеширования в браузере — кешируем на 1 день
        response['Cache-Control'] = 'public, max-age=86400'  # 86400 секунд = 1 день
        response['Expires'] = http_date(datetime.now(tz=timezone.utc).timestamp() + 86400)

        return response

class FlightLocationByCategoryAPIView(APIView):
    def get(self, request, category_name):
        locations = FlightLocation.objects.filter(category__iexact=category_name)
        serializer = FlightLocationListSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)