from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={
                'class': 'border border-gray-300 rounded-lg py-2 px-4 w-full',  # Tailwind CSS classes
                'placeholder': 'City Name'
            }),
        }