from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from weather.models import City, Weather
from weather.weather_api import WeatherManager
import datetime


def weather_tomorrow_post():
    cities = City.objects.all()
    weather_data = []
    current_time = datetime.datetime.now().strftime("%H:%M")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    for citys in cities:
        daily_weather = WeatherManager(citys.name).get_daily_temperature()
        for weather in daily_weather:
            if weather['day'] == current_date:
                day = weather['day']
                average_temperature = int(weather['average_temperature'])
                for hour_weather in weather['hours']:
                    if hour_weather['time'].split(':')[0] == current_time.split(':')[0]:
                        times = hour_weather['time']
                        temp = int(hour_weather['temperature'])
                        weather_data.append(
                            Weather.objects.create(city=citys, day=day, time=times, temp=temp,
                                                   average_temperature=average_temperature)
                        )

    return Response({"detail": "Weather updated successfully"}, status=status.HTTP_200_OK)


def city_list_api(request):
    cities = City.objects.all()
    data = {

        'city': [item for item in cities],

    }

    return render(request, 'weather_torrow.html', data)


def weather_list(request, pk):
    data = {
        "data": Weather.objects.filter(city_id=pk, day=datetime.datetime.now().strftime("%Y-%m-%d"))
    }
    return render(request, 'weather_torrow.html', data)




