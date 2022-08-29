from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
from config import bot
import time
from perser.mouse import parser
from perser.movies import perser


async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'commands: /mem, /quiz, /dice (if u admin game), !pin with reply message')


async def pin(message: types.Message):
    await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)


async def dice(message: types.Message):
    if message.chat.type != "private":
        await bot.send_message(message.chat.id, 'For bot:')
        bot_choice = await bot.send_dice(message.chat.id, emoji='🎲')
        await bot.send_message(message.chat.id, 'For player:')
        player_choice = await bot.send_dice(message.chat.id, emoji='🎲')
        time.sleep(5)
        print(bot_choice.dice.value)
        print(player_choice.dice.value)
        if bot_choice.dice.value > player_choice.dice.value:
            await bot.send_message(message.chat.id, 'Я выиграл, лох')
        elif bot_choice.dice.value == player_choice.dice.value:
            await bot.send_message(message.chat.id, 'МЫ выиграли')
        else:
            await bot.send_message(message.chat.id, 'Игрок выиграл. Ему повезло')
    else:
        await message.reply('пиши только в группе бигбрейн')


async def meme(message: types.message):
    image = ['']
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


async def parser_mouses(message: types.Message):
    data = parser()
    for item in data:
        await bot.send_photo(
            message.from_user.id,
            item['link_photo'], caption=f"{item['link']}\n\n"
                                        f"{item['name']}\n"
                                        f"{item['price']}\n"
                                        f"{item['na sklade']}"
        )


async def parser_movies(message: types.Message):
    data = perser()
    for item in data:
        await bot.send_message(
            message.from_user.id,
            f"{item['link']}\n\n"
            f"{item['name']}\n"
            f"Год выхода: {item['year']}\n\n"
            f"Страна: {item['country']}\n\n"
            f"{item['viewers']}\n"
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(parser_mouses, commands=['mouse'])
    dp.register_message_handler(parser_movies, commands=['movies'])
    dp.register_message_handler(meme, commands=['mem'])
    dp.register_message_handler(quiz1, commands=['quiz'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!/')
    dp.register_message_handler(dice, commands=['dice'])
