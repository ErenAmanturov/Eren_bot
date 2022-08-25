import asyncio
import aioschedule
from aiogram import types, Dispatcher
from config import bot


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await bot.send_message(chat_id=chat_id, text="Напомню")


async def go_lyceum():
    photo = open("media/lol.png", 'rb')
    await bot.send_photo(chat_id=chat_id, photo=photo,
                         caption="Пора тебе в лицей")
    await bot.send_audio(chat_id=chat_id, audio=open('media/xxx.mp3', 'rb'))


async def go_home():
    photo = open("media/golyc.jpg", 'rb')
    await bot.send_photo(chat_id=chat_id, photo=photo,
                         caption="Пора домой из лицея. YOLOOOOOOOOO")
    await bot.send_audio(chat_id=chat_id, audio=open('media/queen.mp3', 'rb'))


async def scheduler():
    aioschedule.every().friday.at('13:00').do(go_home)
    aioschedule.every().sunday.at("18:00").do(go_lyceum)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_hendler_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                lambda word: "Когда в лицей" in word.text)
