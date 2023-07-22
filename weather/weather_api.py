from config.settings import API_OPENWEATHERMAP_ORG, API_TOMORROW
import datetime
import requests
import urllib.request
import json


class WeatherManager:
    API_KEY = API_TOMORROW

    def __init__(self, city):
        self.city = city

    @staticmethod
    def convert_to_datetime(date_str):
        return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

    def get_data(self):
        url = f"https://api.tomorrow.io/v4/weather/forecast?" \
              f"location={self.city}&apikey={self.API_KEY}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:

            return json.loads(response.text)
        else:
            return json.loads(response.text)

    def get_timelines(self):
        res = self.get_data()
        return res.get("timelines")

    def get_daily_data(self):
        timelines = self.get_timelines()
        if timelines:
            return timelines.get("daily")

    def get_hourly_data(self):
        timelines = self.get_timelines()
        if timelines:
            return timelines.get("hourly")

    def get_day_hours_temperature_with_time(self, day_date):
        hourly_data = self.get_hourly_data()
        data = []

        for hour_data in hourly_data:
            time = hour_data.get("time")
            if self.convert_to_datetime(time).date() == day_date.date():
                data.append({
                    "time": self.convert_to_datetime(time).strftime("%H:%M"),
                    "temperature": hour_data["values"].get("temperature")
                })
        return data

    def get_daily_temperature(self):
        data = []
        daily_data = self.get_daily_data()
        if daily_data is None:
            return data
        for day in self.get_daily_data():
            day_values = day.get("values")
            average_temperature = None
            if day_values:
                average_temperature = day_values.get("temperatureAvg")
            day_date = datetime.datetime.strptime(day.get("time"), "%Y-%m-%dT%H:%M:%SZ")
            data.append({
                "day": day_date.strftime("%Y-%m-%d"),
                "average_temperature": average_temperature,
                "hours": self.get_day_hours_temperature_with_time(day_date)}
            )

        return data


def get_daily_weather(city):
    source = urllib.request.urlopen(
        f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_OPENWEATHERMAP_ORG}').read()
    list_of_data = json.loads(source)
    day = datetime.datetime.now().date().strftime("%H:%M")
    daily_weather = [weather for weather in list_of_data['list'] if weather['dt_txt'].split()[0] == day]
    return daily_weather


def get_daily_weather_5_days(city):
    source = urllib.request.urlopen(
        f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_OPENWEATHERMAP_ORG}').read()
    list_of_data = json.loads(source)
    data = []
    for item in list_of_data['list']:
        data.append({
            'temp': int(item['main']['temp'] - 273.15),
            'pressure': item['main']["pressure"],
            'humidity': item['main']['humidity'],
            'clear': item["weather"][0]['main'],
            'description': item["weather"][0]['description'],
            'icon': item["weather"][0]['icon'],
            'day': item['dt_txt'].split()[0],
            'time': item['dt_txt'].split()[1],
            'visibility': item['visibility'],
            'wind_speed': item['wind']['speed'],
            'timezone': list_of_data["city"]['timezone'],
            'sunset': list_of_data["city"]['sunset'],
            'sunrise': list_of_data["city"]['sunrise'],
            'country': list_of_data["city"]['country'],

        })

    return data
