from django.shortcuts import render
import requests

def index(request):
    city = None  # Initialize city variable
    weather = {}

    if request.method == 'POST':
        city = request.POST.get('city')  # Get the city name from the form
        api_key = 'YOUR_API_KEY'  # Replace with your OpenWeatherMap API key
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}'

        response = requests.get(url)
        if response.status_code == 200:
            city_weather = response.json()
            weather = {
                'city': city,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
        else:
            weather = {'error': 'City not found'}

    return render(request, 'weather/index.html', {'weather': weather})