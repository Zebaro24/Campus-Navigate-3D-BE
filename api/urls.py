from django.urls import path
from .views import FlightLocationListAPIView, FlightLocationDetailAPIView, ActiveUniversityModelFileView, \
    FlightLocationByCategoryAPIView

urlpatterns = [
    path('locations/', FlightLocationListAPIView.as_view(),
         name='locations-list'),
    path('locations/<int:pk>/', FlightLocationDetailAPIView.as_view(),
         name='locations-detail'),
    path('active-model-file/', ActiveUniversityModelFileView.as_view(),
         name='active-model-file'),
    path('locations/category/<str:category_name>/', FlightLocationByCategoryAPIView.as_view(),
         name='locations-by-category'),
]
