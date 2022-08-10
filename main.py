from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, dp
import logging
from aiogram.utils import executor
import random


@dp.message_handler(commands=['mem'])
async def meme(message: types.message):
    image = ['media/meme.png', 'media/bot1.jpg', 'media/bot2.png']
    photo = open(random.choice(image), 'rb')
    await bot.send_photo(message.from_user.id, photo=photo)


@dp.message_handler(commands=['quiz'])
async def quiz1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data='button_call_1')
    markup.add(button_call_1)

    question = "Кто из 20-1 группы дединсайд"
    answers = [
        "Али",
        "Абдулла",
        "Бекзат",
        "Алмаз",
        "Эрен"
    ]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=4,
        open_period=10,
        explanation="Это сказал Алмаз",
        reply_markup=markup
    )


@dp.callback_query_handler(lambda call: call.data == "button_call_1")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_2 = InlineKeyboardButton("NEXT", callback_data='button_call_2')
    markup.add(button_call_2)

    question = "Кто учитель 3 месяца"
    answers = [
        "Эсен",
        "Айрас",
        "Алексей",
        "Нурлан"
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        open_period=10,
        explanation="ИЗИ"
    )


@dp.message_handler()
async def echo(message: types.Message):
    if message.text.isdigit():
        await bot.send_message(message.from_user.id, int(message.text) * int(message.text))
    else:
        await bot.send_message(message.from_user.id, message.text)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
