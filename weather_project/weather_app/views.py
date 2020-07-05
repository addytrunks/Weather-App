from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=40bcf8b5d6e70f6380c9f1b4b751b5cd'
    weather_data = []

    err_msg = ''
    message = ''
    message_class = ''
    succ_message=''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['city']
            number_cities = City.objects.filter(city=new_city).count()

            if number_cities == 0:
                r = requests.get(url.format(new_city)).json() 
                if r['cod'] == 200:
                    form.save()
                    succ_message = "City added successfully"
                else:
                    err_msg = "There is no city like that in the world."
            else:
                err_msg = "You have already added  {}".format(new_city)

    form = CityForm()

    cities = City.objects.order_by('-added_at')

    for city in cities:

        r = requests.get(url.format(city)).json()
        
        city_weather = {
            'city': city,
            'temperature':r['main']['temp'],
            'celcius':int(r['main']['temp']-32/1.8),
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
            'country':r['sys']['country'].upper()    
        }

        weather_data.append(city_weather)

    if err_msg:
        message = err_msg
        message_class = "alert-danger"
    
    elif succ_message:
        message = "City has been added to your list successfully"
        message_class = "alert-success"

    print(weather_data)    

    return render(request,'index.html',context={'weather_data':weather_data,
                                                'forms':form,
                                                'message':message,
                                                'message_class':message_class})

def delete_city(request,delete_city):
    City.objects.get(city=delete_city).delete()
    return HttpResponseRedirect('/')