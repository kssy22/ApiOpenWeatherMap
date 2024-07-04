from fastapi import FastAPI
from typing import Optional
from functools import lru_cache
import requests
import datetime

app = FastAPI(
    title="Weather API",
    description="An API to get weather data from OpenWeatherMap",
    version="1.0.0"
)

# Décorateur pour ajouter un cache LRU à la fonction get_weather_data()
@lru_cache(maxsize=128)
def get_weather_data(city, api_key):
    # URL de l'API OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # Envoi de la requête HTTP GET à l'API OpenWeatherMap
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête : {e}")
        return None

    # Vérification du code de statut HTTP
    if response.status_code == 200:
        # Récupération des données au format JSON
        data = response.json()

        # Extraction des informations météorologiques
        weather_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "current_temperature": data["main"]["temp"],
            "min_temperature": data["main"]["temp_min"],
            "max_temperature": data["main"]["temp_max"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "wind_direction": data["wind"]["deg"],
            "pressure": data["main"]["pressure"],
            "weather_description": data["weather"][0]["description"],
            "sunrise": data["sys"]["sunrise"],
            "sunset": data["sys"]["sunset"],
            "cloudiness": data["clouds"],
            "feels_like": data["main"]["feels_like"]
        }

        # Conversion des heures de lever et de coucher de soleil en heure locale
        sunrise_timestamp = weather_data["sunrise"] + data["timezone"]
        sunset_timestamp = weather_data["sunset"] + data["timezone"]
        weather_data["sunrise"] = datetime.datetime.fromtimestamp(sunrise_timestamp).strftime("%H:%M:%S")
        weather_data["sunset"] = datetime.datetime.fromtimestamp(sunset_timestamp).strftime("%H:%M:%S")

        return weather_data
    elif response.status_code == 404:
        print("Ville non trouvée.")
        return None
    else:
        print(f"Erreur : {response.status_code}")
        return None

#Récupère les données météorologiques pour une ville spécifique
@app.get("/weather/{city_name}", response_model=dict)
async def get_weather(city_name: str, api_key: Optional[str] = None):
    """
    Get weather data for a specific city.

    :param city_name: Name of the city to get the weather data for
    :type city_name: str
    :param api_key: API key for OpenWeatherMap (optional)
    :type api_key: str
    :return: Weather data for the specified city
    :rtype: dict
    """
    if api_key is None:
        api_key = "aacc9c2af3f1da550854c1983306e0f1"

    weather_data = get_weather_data(city_name, api_key)

    if weather_data is not None:
        return {
            "Ville": weather_data["city"],
            "Pays": weather_data["country"],
            "Température actuelle": f"{weather_data['current_temperature']}°C",
            "Température minimale": f"{weather_data['min_temperature']}°C",
            "Température maximale": f"{weather_data['max_temperature']}°C",
            "Humidité": f"{weather_data['humidity']}%",
            "Vitesse du vent": f"{weather_data['wind_speed']} m/s",
            "Direction du vent": f"{weather_data['wind_direction']}°",
            "Pression atmosphérique": f"{weather_data['pressure']} hPa",
            "Description générale du temps": weather_data["weather_description"],
            "Heure du lever du soleil": weather_data["sunrise"],
            "Heure du coucher du soleil": weather_data["sunset"],
            "Nébulosité": f"{weather_data["cloudiness"]}%",
            "Sensation thermique": f"{weather_data['feels_like']}°C"
        }
    elif weather_data is None and city_name is not None:
        return {"error": f"La ville {city_name} n'a pas été trouvée."}
    else:
        return {"error": "Erreur lors de la récupération des données météorologiques."}

#Filtre les données par type
@app.get("/weather/{city_name}/{data_type}", response_model=dict)
async def get_weather_by_type(city_name: str, data_type: str, api_key: Optional[str] = None):
    """
    Get weather data for a specific city filtered by data type.

    :param city_name: Name of the city to get the weather data for
    :type city_name: str
    :param data_type: Type of data to filter the weather data by (comma-separated)
    :type data_type: str
    :param api_key: API key for OpenWeatherMap (optional)
    :type api_key: str
    :return: Filtered weather data for the specified city
    :rtype: dict
    """
    if api_key is None:
        api_key = "aacc9c2af3f1da550854c1983306e0f1"

    weather_data = get_weather_data(city_name, api_key)

    if weather_data is not None:
        filtered_data = {key: weather_data[key] for key in weather_data if key in data_type.split(",")}
        return filtered_data
    elif weather_data is None and city_name is not None:
        return {"error": f"La ville {city_name} n'a pas été trouvée."}
    else:
        return {"error": "Erreur lors de la récupération des données météorologiques."}