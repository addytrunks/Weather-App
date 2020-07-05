from django import forms
from .models import City

class CityForm(forms.ModelForm):
    class Meta():
        model = City
        fields = ['city']

        widgets = {
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter a City...','style':'width:350px;','name':'city'})
        }