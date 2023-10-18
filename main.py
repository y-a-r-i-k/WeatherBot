import requests
import datetime
from pprint import pprint
from aiogram import Bot, Dispatcher, executor, types

import cfg

bot = Bot(token=cfg.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['city'])
async def start_command(message: types.Message):
    await message.reply("Отправь мне название города, а я напишу тебе текущую погоду в этом городе.")
    print(f"{message.from_user.id}, Пользователь: @{message.from_user.username}")



@dp.message_handler()
async def get_weather(message: types.Message):

    code_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F38B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={cfg.Weather_KEY}&units=metric"
        )

        data = r.json()
        pprint(data)


        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_des = data["weather"][0]["main"]
        if weather_des in code_smile:
            wd = code_smile[weather_des]

        else:
            wd = f'Weather code: {data["weather"][0]["main"]}'

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) \
              - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"""
*****{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}*****
===============================

👉 Город: {city}
---> Температура: {cur_weather} С° {wd}
---> Влажность воздуха: {humidity} %
---> Давление воздуха: {pressure} мм.рт.ст
---> Скорость ветра: {wind} м/с
---> Время восхода солнца: {sunrise}
---> Время заката солнца: {sunset}
---> Продолжительность светового дня: {day}

===============================
***Удачи!***
""")

    except Exception as ex:
        await message.reply(" \U00002620 Проверьте название города. \U00002620")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)