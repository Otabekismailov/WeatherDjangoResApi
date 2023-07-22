from rest_framework import serializers

from .models import City, WeatherApiApp


class WeatherApiSerializers(serializers.ModelSerializer):
    class Meta:
        model = WeatherApiApp
        fields = ['city', 'day', 'temp', 'time', 'visibility', 'wind_speed', 'sunrise', 'sunset', 'clear',
                  'description',
                  'pressure', 'country', 'timezone', 'humidity', 'icon',]


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)

