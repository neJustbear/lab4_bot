import requests
from config import tg_bot_token, nasa_api
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    button = KeyboardButton(text="Хочу рандомную фотку космоса")
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]])
    await message.reply("Привет, я Nasa-бот. Я могу скинуть тебе рандомную фотку из космоса или фото из космоса по дате(YYYY-MM-DD)", reply_markup=keyboard)

@dp.message_handler(text=['Хочу рандомную фотку космоса'])
async def get_image_rand(message: types.Message):
    if (message.text == "Хочу рандомную фотку космоса"):
        try:
            reqrand = requests.get(
                f"https://api.nasa.gov/planetary/apod?api_key={nasa_api}&count=1")

            data1 = reqrand.json()
            space1 = data1[0]['url']
            await bot.send_photo(message.chat.id, space1)
        except:
            await message.reply("Что-то пошло не так!")


@dp.message_handler()
async def get_image_date(message: types.Message):
    try:
        reqdate = requests.get(
            f"https://api.nasa.gov/planetary/apod?api_key={nasa_api}&date={message.text}"
        )

        data2 = reqdate.json()
        space2 = data2['url']
        await bot.send_photo(message.chat.id, space2)

    except:
        await message.reply("Вы ввели дату неправильно!")


if __name__ == '__main__':
    executor.start_polling(dp)
