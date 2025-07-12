import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class TodayWeatherView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')

        if not lat or not lon:
            return Response({
                "error": "Please provide latitude (lat) and longitude (lon)."
            }, status=400)

        try:
            # Open-Meteo API call
            api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            res = requests.get(api_url)
            data = res.json()

            current_weather = data.get('current_weather', {})
            if not current_weather:
                return Response({"error": "Weather data not available"}, status=404)

            return Response({
                "location": {
                    "latitude": lat,
                    "longitude": lon
                },
                "weather": {
                    "temperature": current_weather.get('temperature'),
                    "windspeed": current_weather.get('windspeed'),
                    "winddirection": current_weather.get('winddirection'),
                    "weathercode": current_weather.get('weathercode'),
                    "time": current_weather.get('time')
                }
            })

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=500)
