from config import dp
import logging
from handlers import client, callback, extra, fsmAdminMenu
from aiogram.utils import executor

client.register_handlers_client(dp)
fsmAdminMenu.register_handlers_fsmadminmenu(dp)
callback.register_handlers_callback(dp)
extra.register_handlers_extra(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
