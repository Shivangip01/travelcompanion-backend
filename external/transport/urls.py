from django.urls import path
from .views import TransportRouteView

urlpatterns = [
    path('routes/', TransportRouteView.as_view(), name='transport-routes'),
    # path('itinerary/', ItineraryView.as_view(), name='itinerary'),

]
