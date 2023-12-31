# Generated by Django 4.2.2 on 2023-06-25 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_alter_weather_average_temperature_alter_weather_temp'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherApiApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('temp', models.FloatField()),
                ('time', models.TimeField()),
                ('visibility', models.IntegerField()),
                ('wind_speed', models.IntegerField()),
                ('sunset', models.IntegerField()),
                ('sunrise', models.IntegerField()),
                ('clear', models.CharField()),
                ('description', models.CharField()),
                ('pressure', models.IntegerField()),
                ('country', models.CharField()),
                ('timezone', models.IntegerField()),
                ('humidity', models.IntegerField()),
                ('icon', models.CharField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shahar', to='weather.city')),
            ],
        ),
    ]
