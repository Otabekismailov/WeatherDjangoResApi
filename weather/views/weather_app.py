from apscheduler.schedulers.background import BackgroundScheduler
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView
from django_apscheduler.jobstores import DjangoJobStore
from weather.models import City, WeatherApiApp, WeatherApi
from weather.serializers import CitySerializers, WeatherApiSerializers
from weather.views import weather_tomorrow_post
from weather.weather_api import get_daily_weather_5_days, get_daily_weather
from rest_framework.response import Response
import uuid


def weather_api_automatic():
    cities = City.objects.all()
    weather_data = []
    for cityDetail in cities:
        daily_weather = get_daily_weather_5_days(cityDetail.name)
        for weather in daily_weather:
            weather_data.append(
                WeatherApiApp.objects.get_or_create(city_id=cityDetail.pk, temp=weather['temp'],
                                                    pressure=weather['pressure'], humidity=weather['humidity'],
                                                    clear=weather['clear'], description=weather['description'],
                                                    icon=weather['icon'], day=weather['day'], time=weather['time'],
                                                    visibility=weather['visibility'],
                                                    wind_speed=weather['wind_speed'],
                                                    timezone=weather['timezone'], sunset=weather['sunset'],
                                                    sunrise=weather['sunrise'], country=weather['country']))
    return Response({"detail": "Weather updated successfully"}, status=status.HTTP_200_OK)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    job_id_1 = str(uuid.uuid4())
    job_id_2 = str(uuid.uuid4())
    scheduler.add_job(weather_api_automatic, 'interval', hours=1, id=job_id_1, jobstore='default')
    scheduler.add_job(weather_tomorrow_post, 'interval', minutes=1, id=job_id_2, jobstore='default')
    scheduler.start(paused=True)


def weather_api_post():
    cities = City.objects.all()
    weather_data = []
    print("progress......")
    for cityDetail in cities:
        daily_weather = get_daily_weather(cityDetail.name)

        for weather in daily_weather:
            day, times = weather['dt_txt'].split()
            temp = int(weather['main']['temp'] - 273.15)

            weather_data.append(
                WeatherApi.objects.update_or_create(city=cityDetail, day=day, time=times, temp=temp)
            )

    return Response({"detail": "Weather updated successfully"}, status=status.HTTP_200_OK)


class CityList(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializers


class WeatherApiViews(ListAPIView):
    queryset = WeatherApiApp.objects.all()
    serializer_class = WeatherApiSerializers
    lookup_field = 'pk'

    def get_queryset(self):
        city_id = self.kwargs.get('pk')
        queryset = self.queryset.filter(city_id=city_id)
        if queryset.count() == 0:
            raise Http404
        return queryset
