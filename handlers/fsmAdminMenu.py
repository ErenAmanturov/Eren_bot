from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMIN
from keyboards.client_kb import cancel_markup


class FSMAdmin(StatesGroup):
    photo_of_the_dish = State()
    title_of_the_dish = State()
    description_of_the_dish = State()
    price_of_the_dish = State()


async def fsm_menu_start(message: types.Message):
    if message.from_user.id in ADMIN:
        await FSMAdmin.photo_of_the_dish.set()
        await message.answer(f"Здравствуй, менеджер {message.from_user.full_name} "
                             f"Как выглядит ваше блюдо?", reply_markup=cancel_markup)
    else:
        await message.reply("Пишите в личку!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as menu:
        menu['id'] = message.from_user.id
        menu['username'] = f"@{message.from_user.username}"
        menu['Photo of the Dish'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Название данного блюда")


async def load_title(message: types.Message, state: FSMContext):
    async with state.proxy() as menu:
        menu['Title of the Dish'] = message.text
    await FSMAdmin.next()
    await message.answer('Опишите ваше блюдо')


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as menu:
        if len(message.text) < 10 and len(message.text) < 20:
            await message.reply('Описание должно состоять больше 10 символов и меньше 20')
        else:
            menu['Description of the Dish'] = message.text
            await FSMAdmin.next()
            await message.answer('Сколько будет стоит ваше блюдо')


async def load_price(message: types.Message, state: FSMContext):
    try:
        if int(message.text) < 20000:
            async with state.proxy() as menu:
                menu['Price of the Dish'] = int(message.text)
                await bot.send_photo(message.from_user.id, menu['Photo of the Dish'],
                                     caption=f"Название вашего блюда: {menu['Title of the Dish']}\n"
                                             f"Цена вашего блюда: {menu['Price of the Dish']}")
                await bot.send_message(message.from_user.id, f"Описание вашего блюда: {menu['Description of the Dish']}")
                await state.finish()
                await message.answer(f"На этом все, менеджер {message.from_user.first_name}")
        else:
            await bot.send_message(message.chat.id, 'Цена не может быть настолько высокой')
    except:
        await bot.send_message(message.from_user.id, 'Любые символы кроме цифр запрещены. Пожалуйста вводите цифры')


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer(f'Вы отменили добавление нового блюда, менеджер {message.from_user.first_name}')


def register_handlers_fsmadminmenu(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands='cancel')
    dp.register_message_handler(cancel_registration, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(fsm_menu_start, commands=['menu'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo_of_the_dish,
                                content_types=['photo'])
    dp.register_message_handler(load_title, state=FSMAdmin.title_of_the_dish)
    dp.register_message_handler(load_description, state=FSMAdmin.description_of_the_dish)
    dp.register_message_handler(load_price, state=FSMAdmin.price_of_the_dish)

