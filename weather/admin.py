from django.contrib import admin

from weather.models import City, WeatherApi,WeatherApiApp

# Register your models here.
admin.site.register(City)
admin.site.register(WeatherApi)
admin.site.register(WeatherApiApp)