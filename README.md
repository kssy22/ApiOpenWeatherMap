# API OpenWeatherMap

Ce projet est une API qui permet de récupérer les données météorologiques d'une ville donnée en utilisant l'API OpenWeatherMap.

# Pour exécuter le projet

Il faut lancer l'application avec la commande :
uvicorn main:app --reload

L'API sera disponible sur `http://localhost:8000` et ainsi executer et tester sur Postman.

# Pour récupérer les données météorologiques pour une ville spécifique

Pour récupérer les données météorologiques pour une ville spécifuque, il faut envoyer une requête GET à `/weather/{city_name}`.

Par exemple :
http://localhost:8000/weather/Paris

Cela retournera les données météorologiques de Paris dans un format JSON.

# Pour filtrer les données météorologiques par type

Pour filtrer les données météorologiques par type, il faut envoyer une requête GET à `/weather/{city_name}/data_type}`.

Par exemple :
http://localhost:8000/weather/Paris/temperature,humidity

Cela retournera la température actuelle et l'humidité de Paris dans un format JSON.

# Pour tester l'API

Il faut utiliser la commande :
pytest

Cette commande lancera les tests dans le fichier test_weather.py.

# PS : Cependant, je n'ai pas très bien réussi les tests car pas on ne les as pas vu en cours.