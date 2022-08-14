from aiogram import types, Dispatcher
from config import bot
from config import ADMIN
import random
import time


async def game(message: types.Message):
    games = ['🎯', '🎳', '🎲', '🎰', '🏀', '⚽️']
    r_games = random.choice(games)
    if message.text.startswith('game'):
        if message.chat.type != "private":
            if message.from_user.id not in ADMIN:
                await message.reply("Эта игра только для админов")
            else:
                await bot.send_message(message.chat.id, 'For bot:')
                bot_choice = await bot.send_dice(message.chat.id, emoji=r_games)
                await bot.send_message(message.chat.id, 'For player:')
                player_choice = await bot.send_dice(message.chat.id, emoji=r_games)
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
            await message.reply("Пиши в группе!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(game)
