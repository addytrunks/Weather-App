from django.urls import path
from weather_app import views

urlpatterns = [
    path('',views.home,name='home'),
    path('delete/<delete_city>',views.delete_city,name='delete_city')
]
