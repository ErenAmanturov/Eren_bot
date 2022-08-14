from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, Dispatcher
import random


async def pin(message: types.Message):
    await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)


async def meme(message: types.message):
    image = ['media/meme.png', 'media/bot1.jpg', 'media/bot2.png']
    photo = open(random.choice(image), 'rb')
    await bot.send_photo(message.chat.id, photo=photo)


async def quiz1(message: types.Message):

    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data='button_call_1')
    markup.add(button_call_1)

    question = "Кто самый умный в классе"
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
        correct_option_id=3,
        open_period=10,
        explanation="Это сказал Алмаз",
        reply_markup=markup
    )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(meme, commands=['mem'])
    dp.register_message_handler(quiz1, commands=['quiz'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
