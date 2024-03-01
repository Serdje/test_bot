import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.types import Message
from aiogram.types import URLInputFile
import requests
import time

logging.basicConfig(level=logging.INFO)
TOKEN_API = '7086099829:AAFi5sdy4pRBFwwmZ0skek92r1y3YmXwZUU'
bot = Bot(TOKEN_API)
dp = Dispatcher()

kb = [
    [types.KeyboardButton(text="Хочу песика!")],
    [types.KeyboardButton(text="Скинь кота!")]
]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Кого выбираешь?",
    is_persistent=True,
    one_time_keyboard=False
)


@dp.message(F.text, Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer(f"Выбери, кого отправить.", reply_markup=keyboard)


@dp.message(F.text == 'Хочу песика!')
async def get_dog(message: types.Message):
    request = requests.get('https://dog.ceo/api/breeds/image/random')
    link = str(request.json()['message'])
    image_from_url = URLInputFile(link)
    await message.answer_photo(
        image_from_url,
        # caption="Фото песика!"
    )
    time.sleep(3.5)


@dp.message(F.text == 'Скинь кота!')
async def get_cat(message: types.Message):
    request = requests.get('https://api.thecatapi.com/v1/images/search')
    link = str(request.json()[0]['url'])
    image_from_url = URLInputFile(link)
    if link.split('.')[-1] == 'gif':
        await message.answer_animation(
            image_from_url
        )
    else:
        await message.answer_photo(
            image_from_url,
        )
    time.sleep(3.5)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
