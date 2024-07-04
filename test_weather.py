from main import app

import pytest
import httpx

pytestmark = pytest.mark.asyncio

#Ce test vérifie que l'endpoint '/weather/{city_name} renvoie les bonnes données pour une ville donnée
@pytest.mark.asyncio
async def test_get_weather():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/weather/Paris")
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "Paris"
        assert data["country"] == "FR"
        assert "current_temperature" in data
        assert "min_temperature" in data
        assert "max_temperature" in data
        assert "humidity" in data
        assert "wind_speed" in data
        assert "wind_direction" in data
        assert "pressure" in data
        assert "weather_description" in data
        assert "sunrise" in data
        assert "sunset" in data
        assert "cloudiness" in data
        assert "feels_like" in data

#Ce test vérifie que l'endpoint /weather/{city_name}/{data_type} renvoie les bonnes données pour une ville et un type de données donnés
@pytest.mark.asyncio
async def test_get_weather_by_type():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/weather/Paris/current_temperature,humidity")
        assert response.status_code == 200
        data = response.json()
        assert "current_temperature" in data
        assert "humidity" in data
        assert len(data) == 2
