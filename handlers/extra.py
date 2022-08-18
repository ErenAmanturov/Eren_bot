from aiogram import types, Dispatcher
from config import bot, ADMIN
import random


async def echo(message: types.Message):
    games = ['🎯', '🎳', '🎲', '🎰', '🏀', '⚽️']
    r_games = random.choice(games)
    if message.text.startswith('game'):
        if message.chat.type != "private":
            if message.from_id in ADMIN:
                await bot.send_dice(message.chat.id, emoji=r_games)
            else:
                await message.reply('Ты не мой босс')
        else:
            await message.reply('пиши только в группе бигбрейн')
    if message.text.isdigit():
        await bot.send_message(message.chat.id, int(message.text) * int(message.text))
    else:
        await bot.send_message(message.chat.id, message.text)


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
