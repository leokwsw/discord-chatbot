import json
import os

import requests

from src.logger import logger


async def get_weather(city: str):
    logger.log(level=0, msg="Fetching weather with city " + city)

    if len(city) <= 0:
        return json.dumps({})
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={os.getenv('OPEN_WEATHER_API')}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        return json.dumps({
            "location": city,
            "temperature": temp,
            "unit": "metric"
        })
    else:
        print('Error fetching weather data')
        print("response", response)
        print(response)
        return json.dumps({})
