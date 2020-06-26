import pyowm
import random
import asyncio

owm = pyowm.OWM("781d1e03a79414b0374c469c3a1b1cd7")
mgr = owm.weather_manager()
WEATHER_KEY = "781d1e03a79414b0374c469c3a1b1cd7"

city_id = 554840

translate_list_detailed = {
    "clear sky": "Ясно",
    "few clouds": "Небольшая облачность",
    "scattered clouds": "Облачно",
    "broken clouds": "Тучи",
    "shower rain": "Ливень",
    "rain": "Дождь",
    "thunderstorm": "Гроза",
    "snow": "Снег",
    "mist": "Лёгкий туман"
}

translate_list = {
    "Thunderstorm" : "Гроза",
    "Drizzle": "Бог испольует пульверизатор",
    "Rain": "Дождь",
    "Snow": "Снег",
    "Mist": "Лёгкий туман",
    "Smoke": "Смог",
    "Haze": "Дымка",
    "Dust": "Пыльно",
    "Fog": "Туман",
    "Sand": "Песок?..",
    "Ash": "Пепел",
    "Squall": "Шквал",
    "Tornado": "Торнадо",
    "Clear": "Ясно",
    "Clouds": "Облачно"
}

directions = [
    "Северный",
    "Северо-восточный",
    "Восточный",
    "Юго-восточный",
    "Южный",
    "Юго-западный",
    "Западный",
    "Северо-западный",
    "Северный"
]

def wind_direction(degree):
    return directions[int((degree % 360)/ 45) + 1]

def get_weather(city = None):
    try:
        if city == None:
            temp = mgr.weather_at_id(city_id)
        else:
            temp = mgr.weather_at_place(city)
    except pyowm.commons.exceptions.NotFoundError:
        return False
    
    status = translate_list_detailed.get(temp.weather.detailed_status, False)
    if not status:
        status = translate_list.get(temp.weather.status, False)

    temperature = temp.weather.temperature("celsius")
    wind_data = temp.weather.wind()
    wind = "{0}, {1} м/с".format(wind_direction(wind_data.get("deg")), wind_data.get("speed"))
    ret_string = "Погода в: {0.location.name}\n{4}Температура: {1:.1f}°C, ощущается как: {2:.1f}°C\nВлажность: {3}\nВетер: {5}{6}".format(temp, temperature.get("temp"), temperature.get("feels_like") , temp.weather.humidity, status + "\n" if status else "", wind, "\nПриятной прогулки! :3" if random.randint(0, 10) == 0 else "")
    return ret_string


    

if __name__ == "__main__":
    print(get_weather())