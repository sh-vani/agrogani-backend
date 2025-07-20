import requests
from django.conf import settings

def fetch_weather_data(lat, lon):
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        return {"error": data.get("message", "Failed to fetch weather")}

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind": data["wind"]["speed"]
    }
