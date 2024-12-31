from django.shortcuts import render
import requests
from .models import City

def index(request):
    cities = City.objects.all()  # Retrieve all cities from the database
    weather = {}

    if request.method == 'POST':
        city_name = request.POST.get('city')  # Get the city name from the form
        api_key = '49f21af64f749234c18f1726659bf7a1'  # Your OpenWeatherMap API key as a string
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={api_key}'

        response = requests.get(url)
        if response.status_code == 200:
            city_weather = response.json()
            weather = {
                'city': city_name,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
        else:
            weather = {'error': 'City not found'}

    return render(request, 'weather/index.html', {'weather': weather, 'cities': cities})