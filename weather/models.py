from django.db import models
from django.utils.text import slugify


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(
            self, *args, **kwargs
    ):
        self.slug = slugify(self.name)
        return super().save(*args, *kwargs)

    class Meta:
        verbose_name_plural = 'City'


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city')
    day = models.DateField()
    temp = models.IntegerField()
    time = models.TimeField()
    average_temperature = models.IntegerField()


class WeatherApi(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cityapi')
    day = models.DateField()
    temp = models.IntegerField()
    time = models.TimeField()


class WeatherApiApp(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='shahar')
    day = models.DateField()
    temp = models.FloatField()
    time = models.TimeField()
    visibility = models.IntegerField()
    wind_speed = models.IntegerField()
    sunset = models.IntegerField()
    sunrise = models.IntegerField()
    clear = models.CharField()
    description = models.CharField()
    pressure = models.IntegerField()
    country = models.CharField()
    timezone = models.IntegerField()
    humidity = models.IntegerField()
    icon = models.CharField()
    def __str__(self):
        return self.city
