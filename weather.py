import json
import requests
import sys
import config

def get_json_data_for_city(city):
    """Get weather data in JSON-format for a given city.

    Keyword arument:
    city -- the city to find weather data for
    """
    request_url = config.weather['base_url'] + city + '&appid=' + config.weather['apikey']
    r = requests.request('GET', request_url)
    return json.loads(r.text)


def kelvin_to_celcius(temp):
    """Convert from kelvin to celcius.

    Keyword argument:
    temp -- kelvin temperature
    """
    return temp - 273.15

def get_name(weather_data):
    """Get the name of a city given JSON data.

    Keyword argument:
    weather_data -- JSON data for a city
    """
    return weather_data['name']

def get_description(weather_data):
    """Get weather description for a city given JSON data.

    Keyword argument:
    weather_data -- JSON data for a city
    """
    return weather_data['weather'][0]['description']

def get_weather_string(city):
    """Get a string of weather information for a city, given city name.

    Keyword argument:
    city -- city name string
    """
    data = get_json_data_for_city(city)
    temp = get_temp(data)
    name = get_name(data)
    description = get_description(data)

    return 'Temperature in {}: {} degrees celcius. Weather description: {}'.format(name, temp, description)

def get_temp(weather_data):
    """Get the temperature for a city given JSON data.

    Keyword argument:
    weather_data -- JSON data fro a city
    """
    kelvin_temp = weather_data['main']['temp']
    return kelvin_to_celcius(float(kelvin_temp))
