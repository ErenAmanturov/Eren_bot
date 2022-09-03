import asyncio
from config import dp, bot, URL
import logging
from handlers import client, callback, extra, fsmAdminMenu, notification, inline
from database import bot_db
from aiogram.utils import executor
from decouple import config


async def on_startup(_):
    await bot.set_webhook(URL)
    asyncio.create_task(notification.scheduler())
    bot_db.sql_create()


async def on_shutdown(dp):
    await bot.delete_webhook()


client.register_handlers_client(dp)
callback.register_handlers_callback(dp)
fsmAdminMenu.register_handlers_fsmadminmenu(dp)
notification.register_hendler_notification(dp)
extra.register_handlers_extra(dp)
inline.register_handler_inline(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path="",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=config("PORT", cast=int)
    )
