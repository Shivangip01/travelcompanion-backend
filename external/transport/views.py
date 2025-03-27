# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status


# class TransportRouteView(APIView):
#     def get(self, request):
#         from_city = request.query_params.get('from')
#         to_city = request.query_params.get('to')

#         if not from_city or not to_city:
#             return Response({'error': 'from and to parameters are required'}, status=400)

#         try:
#             #external_url = f"https://classmate-api.com/api/transport/routes?from={from_city}&to={to_city}"
#             external_url = f"http://127.0.0.1:8001/api/routes/?from={from_city}&to={to_city}"
#             response = requests.get(external_url)
#             data = response.json()
#             return Response(data)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from travel.models import Place
from travel.serializers import PlaceSerializer
from django.conf import settings # ✅ For API key


UNSPLASH_URL = "https://api.unsplash.com/search/photos"

class TransportRouteView(APIView):
    def get(self, request):
        from_city = request.query_params.get('from')
        to_city = request.query_params.get('to')

        if not from_city or not to_city:
            return Response({'error': 'from and to parameters are required'}, status=400)

        # Step 1: Get destination info from your own DB
        place = Place.objects.filter(name__iexact=to_city).first()
        if not place:
            return Response({'error': f"No place found with name '{to_city}'"}, status=404)
        
        # --- WEATHER FETCH ---
        weather = {}

        # --- IMAGE FETCH ---
        image_urls = []

        # Step 2: Try fetching transport data from classmate API
        transport_data = []
        try:
            transport_url = f"http://127.0.0.1:8001/api/routes/?from={from_city}&to={to_city}"
            response = requests.get(transport_url)
            response.raise_for_status()
            transport_data = response.json()

            # If transport_data is empty, set a message
            if not transport_data:
                transport_data = "Transport not available right now"
            
##################  WHEATHER API LOGIC #################################
            weather_url = (
                f"http://api.openweathermap.org/data/2.5/weather?q={to_city}"
                f"&appid={settings.OPENWEATHER_API_KEY}&units=metric"
            )
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if weather_response.status_code == 200:
                weather = {
                    "temperature": f"{weather_data['main']['temp']}°C",
                    "condition": weather_data['weather'][0]['description'],
                }
            else:
                weather = "Weather data not available right now."
################### UNPLASH API LOGIC  ########################################
            unsplash_response = requests.get(
                UNSPLASH_URL,
                params={
                    'query': to_city,
                    'client_id': settings.UNSPLASH_ACCESS_KEY,
                    'per_page': 5,
                }
            )
            if unsplash_response.status_code == 200:
                data = unsplash_response.json()
                image_urls = [img['urls']['regular'] for img in data['results']]
            else:
                image_urls = ["No images found"]

        except Exception as e:
            # If error, fallback to showing destination info + notice
            
            weather = "Weather service error"
            image_urls = ["Image service error"]
            transport_data = "Transport not available right now"

        # Step 3: Return both destination and transport message or list
        return Response({
            'destination': PlaceSerializer(place).data,
            'transport_options': transport_data,
            'weather': weather,
            'images': image_urls
        })
