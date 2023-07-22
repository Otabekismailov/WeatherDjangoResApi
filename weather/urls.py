from django.urls import path
from .views import weather_api_automatic, CityList, WeatherApiViews
from .views import weather_api_post, weather_tomorrow_post, city_list_api,weather_list


urlpatterns = [
    path('create-api/', weather_api_post, name='automatic-create-weather'),
    path('create/', weather_tomorrow_post, name='automatic-create-weather-two'),
    path('', city_list_api, name='city'),
    # path('weather/<int:pk>/', weather_list, name='weather-list'),
    path('weather_automatic/', weather_api_automatic, name='weather-list-automatic'),
    path('city-list/', CityList.as_view(), name='city-list-api'),
    path('weather-list/<int:pk>/', WeatherApiViews.as_view(), name='weather-list-api'),
]


