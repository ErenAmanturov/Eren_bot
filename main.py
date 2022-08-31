import asyncio
from config import dp
import logging
from handlers import client, callback, extra, fsmAdminMenu, notification, inline
from database import bot_db
from aiogram.utils import executor


async def on_startup(_):
    asyncio.create_task(notification.scheduler())
    bot_db.sql_create()


client.register_handlers_client(dp)
callback.register_handlers_callback(dp)
inline.inline_google_handler(dp)
fsmAdminMenu.register_handlers_fsmadminmenu(dp)
notification.register_hendler_notification(dp)
extra.register_handlers_extra(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
