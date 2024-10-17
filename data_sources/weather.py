import os
import requests
import datetime
from more_itertools import consecutive_groups

from telegram.ext import ContextTypes

import utils

def weather_icon(icon: str) -> str:
    match icon:
        case "01d": return "☀️"
        case "02d": return "🌤️"
        case "03d": return "🌥️"
        case "04d": return "☁️"
        case "09d": return "🌧️"
        case "10d": return "🌦️"
        case "11d": return "⛈️"
        case "13d": return "🌨️"
        case "50d": return "🌫️"

        case _: return "🌙"  # hack

def get_temp(data) -> str:
    """Gets the temperature data from the last 24 hours"""

    current = data["current"]["temp"]
    feels_like = data["current"]["feels_like"]
    max = data["daily"][0]["temp"]["max"]
    min = data["daily"][0]["temp"]["min"]

    icon = "❄️" if current < 12 else "🌡️" if current < 18 else "🔥"

    return f"{icon} The current temperature is {current}°C, but it feels like {feels_like}°C. The high for today is {max}°C and the low is {min}°C."

def get_rain(data) -> str:
    rain_times = []
    end_of_day = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

    for hour in data["hourly"]:
        if hour["dt"] > end_of_day.timestamp():
            break
        if hour["weather"][0]["main"] == "Rain":
            time = datetime.datetime.fromtimestamp(hour["dt"]).hour
            rain_times.append(time)

    # Prettify the output
    if rain_times == []:
        return "🌞 No rain is expected for the rest of the day."
    
    str = "🌧️ Rain is expected "

    rain_times = [list(group) for group in consecutive_groups(rain_times)]
    for i, group in enumerate(list(rain_times)):
        _str = ""
        group = list(group)
        if len(group) == 1:
            _str += f"at {group[0]}:00"
        else:
            _str += f"from {group[0]}:00 to {group[-1]}:00"

        if len(rain_times) == 1:
            return str + _str + "."
        elif i == len(rain_times) - 1:
            str = str + "and " + _str + "."
        else:
            str = str + _str + ", "

    return str

async def today_forecast(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gets the rain data from the last 24 hours"""
    assert context.user_data is not None

    chat_id = context.user_data["user_id"]

    token = os.getenv("OWM_TOKEN")
    lat, lon = await utils.get_loc(context)

    resp = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&APPID={token}&units=metric")

    if resp.status_code != 200:
        await context.bot.send_message(chat_id=chat_id, text="Something went wrong when getting the weather. Please try again later.")
        return

    data = resp.json()
    forecast = f"Today's forecast is {data['daily'][0]['weather'][0]['description']}."
    icon = weather_icon(data["daily"][0]["weather"][0]["icon"])
    temp = get_temp(data)
    rain = get_rain(data)

    await context.bot.send_message(chat_id=chat_id, text=f"\
{icon} {forecast}\n\
{temp}\n\
{rain}")

