import sqlite3
import random

from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных под   ключена!")

    db.execute("CREATE TABLE IF NOT EXISTS ADMINmenu "
               "(Photo TEXT, Title TEXT PRIMARY KEY, Description TEXT, Price INTEGER)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as menu:
        cursor.execute("INSERT INTO ADMINmenu VALUES "
                       "(?,?,?,?)",
                       tuple(menu.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM ADMINmenu").fetchall()
    random_user = random.choice(result)
    await bot.send_photo(message.from_user.id, random_user[0],
                         caption=f'Title: {random_user[1]}'
                                 f'Description: {random_user[2]}'
                                 f'Price: {random_user[3]}')


async def sql_command_all():
    return cursor.execute("SELECT * FROM ADMINmenu").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM ADMINmenu WHERE Title == ?", (id,))
    db.commit()
