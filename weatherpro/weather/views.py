from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
    form = CityForm()  # Initialize the form
    cities = City.objects.all()  # Retrieve all cities from the database
    weather_data = []  # Initialize a list to hold weather data for each city

    # Fetch weather data for each city in the database
    for city in cities:
        api_key = '49f21af64f749234c18f1726659bf7a1'  # Your OpenWeatherMap API key as a string
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city.name}&units=imperial&appid={api_key}'  # Assuming city has a 'name' attribute

        city_weather = requests.get(url).json()  # Request the API data and convert the JSON to Python data types

        if city_weather.get('main'):  # Check if the response contains weather data
            weather = {
                'city': city.name,  # Use the city name from the database
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
            weather_data.append(weather)  # Add the data for the current city into our list

    # Handle form submission for adding a new city
    if request.method == 'POST':
        form = CityForm(request.POST)  # Bind the form with the POST data
        if form.is_valid():  # Check if the form is valid
            city_name = form.cleaned_data['city']  # Get the city name from the form
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={api_key}'

            response = requests.get(url)
            if response.status_code == 200:
                city_weather = response.json()
                new_weather = {
                    'city': city_name,
                    'temperature': city_weather['main']['temp'],
                    'description': city_weather['weather'][0]['description'],
                    'icon': city_weather['weather'][0]['icon']
                }
                weather_data.append(new_weather)  # Add the new city's weather data to the list
            else:
                error_message = 'City not found'
                weather_data.append({'error': error_message})  # Add an error message if the city is not found

    context = {'weather_data': weather_data, 'form': form}  # Prepare context for rendering
    return render(request, 'weather/index.html', context)  # Render the index.html template with the context