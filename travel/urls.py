from django.urls import path
from .views import PlaceListCreateAPIView, PlaceRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('places/', PlaceListCreateAPIView.as_view(), name='place-list-create'),
    path('places/<int:pk>/', PlaceRetrieveUpdateDestroyAPIView.as_view(), name='place-detail'),
]