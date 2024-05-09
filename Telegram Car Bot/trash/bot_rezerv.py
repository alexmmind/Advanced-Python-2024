import asyncio
import logging
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config_reader import config
from random import randint
from aiogram.filters import Command
from aiogram.utils.formatting import Text, Bold
# import telebot
# модуль работы со временем
from datetime import datetime, timezone, timedelta
# модуль для работы с базой данных
import sqlite3 as sl



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Для записей с типом Secret* необходимо 
# вызывать метод get_secret_value(), 
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        conn = sl.connect('database.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO reports VALUES("{message.from_user.id}")')#, "@{message.from_user.username}")')
        conn.commit()
    except Exception as e:
        print('❌❌❌❌❌❌❌❌❌❌')
        print(e)
        conn = sl.connect('database.db')
        cur = conn.cursor()
        # cur.execute('''
        #                 CREATE TABLE IF NOT EXISTS users (
        #                     user_id INTEGER,
        #                     username TEXT
        #                 )
        #             ''')
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS reports (
                        datetime VARCHAR(40) PRIMARY KEY,
                        date VARCHAR(20),
                        id VARCHAR(200),
                        name VARCHAR(200),
                        text VARCHAR(500)
                    );
                """)
        # cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}")')
        conn.commit()

    msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
           " о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
           " Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
           " нажмите 'Старт' чтобы начать:")
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Старт \U0001F697",
        callback_data="start_bot")
    )

    await message.answer(msg, reply_markup=builder.as_markup())

# обрабатываем входящий отчёт пользователя

@dp.message(F.text)
async def func(message: Message):
    # подключаемся к базе
    con = sl.connect('database.db')
    # подготавливаем запрос
    sql = 'INSERT INTO reports (datetime, date, id, name, text) values(?, ?, ?, ?, ?)'
    # получаем дату и время
    now = datetime.now(timezone.utc)
    # и просто дату
    date = now.date()
    # формируем данные для запроса
    data = [
        (str(now), str(date), str(message.from_user.id), str(message.from_user.username), str(message.text[:500]))
    ]
    # добавляем с помощью запроса данные
    with con:
        con.executemany(sql, data)
    # отправляем пользователю сообщение о том, что отчёт принят
    # bot.send_message(message.from_user.id, 'Принято, спасибо!', parse_mode='Markdown')
    await message.answer(message.from_user.id, 'Принято, спасибо!')#, parse_mode='Markdown')#, reply_markup=builder.as_markup())


# @dp.message(F.text)
# async def echo_with_time(message: Message):
#     # Получаем текущее время в часовом поясе ПК
#     time_now = datetime.now().strftime('%H:%M')
#     # Создаём подчёркнутый текст
#     added_text = html.underline(f"Создано в {time_now}")
#     # Отправляем новое сообщение с добавленным текстом
#     await message.answer(f"{message.text}\n\n{added_text}", parse_mode="HTML")
# # @dp.message_handler(content_types=['text'])
# # async def process_entry(message: types.Message):

@dp.message(F.text)
async def func1(message: Message):
    entry_text = message.text
    # Generate unique ID based on date and time
    entry_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # # Split the entry text into individual words
    # words = entry_text.split()

    # # Process the words (replace this with your desired logic)
    # for word in words:
    #     print(f"Processing word: {word}")       # Your custom logic here, e.g., analysis, filtering, etc.

    # # Store the entry ID and text (you can use a database or any suitable storage method)
    # # ... (your storage logic here)

    await message.answer(f"Запись сохранена. ID записи: {entry_id}, запись: {entry_text}")


@dp.message(Command("profile"))
async def get_profile(msg: types.Message):
    conn = sl.connect(f'database.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users WHERE id = "{msg.from_user.id}"')
    result = cur.fetchall()
    await bot.send_message(msg.from_user.id, f'ID = {list(result[0])[0]}\nUserName = {[list(result[0])[1]][0]}')
    #Да, я художник, я так вижу, а кто шарит, может мне подсказать, буду благодарен

from keyboards import start_bot_kbrd, make_inline_kbrd, gen_markup

@dp.callback_query(F.data == "start_bot")
async def start_bot(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = make_inline_kbrd(start_bot_kbrd)
    # builder = InlineKeyboardBuilder()
    # builder.add(types.InlineKeyboardButton(
    #     text="Создать запись \U0001F4DD",
    #     callback_data="create_note")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="Найти запись \U0001F50E",
    #     callback_data="find_note")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="Посмотреть статистику \U0001F4CA",
    #     callback_data="view_statistics")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="Добавить напоминание \U0001F4C6",
    #     callback_data="reminder")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="На главную \U0001F3E0",
    #     callback_data="start_bot")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="Помощь \U0001F91D",
    #     callback_data="help")
    # )
    # builder.adjust(2)
    print(type(start_bot_kbrd))
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=builder.as_markup()#gen_markup(start_bot_kbrd, 2)#make_inline_kbrd(start_bot_kbrd)#builder.as_markup()

    )


@dp.callback_query(F.data == "create_note")
async def create_note(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Заправка/расход \U000026FD",
        callback_data="fuel")
    )
    builder.add(types.InlineKeyboardButton(
        text="Масло \U0001F6E2",
        callback_data="oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="Покупка запчастей \U00002699",
        callback_data="parts")
    )
    builder.add(types.InlineKeyboardButton(
        text="Другая заметка \U0001F4DD",
        callback_data="other_note")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )
    builder.adjust(2)
    await callback.message.answer(
        "Выберите тип заметки",
        reply_markup=builder.as_markup()
    )

from aiogram.filters import Command, StateFilter
# from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiogram.dispatcher
# from aiogram.dispatcher import FSMContext
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

class MakeNote(StatesGroup):
    chosing_note_type = State()
    make_note_state = State()

from aiogram.filters import Command, StateFilter
# from aiogram.fsm.context import FSMContext
from aiogram import Router, F
router = Router()  # [1]

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# from  note import type_note
# def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
#     """
#     Создаёт реплай-клавиатуру с кнопками в один ряд
#     :param items: список текстов для кнопок
#     :return: объект реплай-клавиатуры
#     """
#     row = [KeyboardButton(text=item) for item in items]
#     return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)



# @router.message(StateFilter(None), Command("food"))
# async def cmd_food(message: Message, state: FSMContext):
#     await message.answer(
#         text="Выбирите тип заметки",
#         reply_markup=make_row_keyboard(type_note)
#     )
#     # Устанавливаем пользователю состояние "выбирает название"
#     await state.set_state(OrderFood.choosing_food_name)




# from aiogram.dispatcher.filters.state import State, StatesGroup


@dp.callback_query(F.data == "fuel")
async def create_note(callback: types.CallbackQuery):
    await callback.message.delete()
    # builder = InlineKeyboardBuilder()
    # builder.add(types.InlineKeyboardButton(
    #     text="Заправка/расход \U000026FD",
    #     callback_data="fuel")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="Масло \U0001F6E2",
    #     callback_data="oil")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="Покупка запчастей \U00002699",
    #     callback_data="parts")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="Другая заметка \U0001F4DD",
    #     callback_data="other_note")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="На главную \U0001F3E0",
    #     callback_data="start_bot")
    # )
    # builder.adjust(2)
    await callback.message.answer(
        "введите текст заметки",
        # reply_markup=builder.as_markup()
    )
    func1()



@dp.callback_query(F.data == "find_note")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=" По тегу \U00000023",
        callback_data="find_by_tag")
    )
    builder.add(types.InlineKeyboardButton(
        text="По дате \U0001F4C5",
        callback_data="find_by_date")
    )
    builder.add(types.InlineKeyboardButton(
        text="По тегу и дате \U0001F50E",
        callback_data="find_by_tag_and_date")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )
    builder.adjust(2)
    await callback.message.answer(
        "Выберите тип поиска",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "view_statistics")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=" По тегу \U00000023",
        callback_data="view_by_tag")
    )
    builder.add(types.InlineKeyboardButton(
        text="По дате \U0001F4C5",
        callback_data="view_by_date")
    )
    builder.add(types.InlineKeyboardButton(
        text="По тегу и дате \U0001F50E",
        callback_data="view_by_tag_and_date")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )
    builder.adjust(2)
    await callback.message.answer(
        "Выберите тип фильтрации",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "reminder")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    # builder.add(types.InlineKeyboardButton(
    #     text=" По тегу \U00000023",
    #     callback_data="view_by_tag")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="По дате \U0001F4C5",
    #     callback_data="view_by_date")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="По тегу и дате \U0001F50E",
    #     callback_data="view_by_tag_and_date")
    # )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )

    builder.adjust(1)
    await callback.message.answer(
        "Введите название напоминания:",
        reply_markup=builder.as_markup()
    )
    reminder_name()

@dp.message(Command("hello"))
async def reminder_name(message: Message):
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(
        **content.as_kwargs()
    )

@dp.callback_query(F.data == "help")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()

    msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
           " о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
           " Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
           "\n"
           "Вы можете создать заметку о своем автомобиле, содержащую информацию о расходе топлива, замене или доливке масла, покупке запчастей а также прочие заметки,"
           " можете добавить напоминание на любую дату, например купить запчасть или поменять масло,"
           " также вы можете искать заметки по дате или их тегу, а также просматривать статистику по оставленным данным о вашем автомоибле."
           " Например средний расход топлива или график изменения расхода за год.\n"
           "Воспользуйтесь одной из кнопок ниже, чтобы начать:")
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Создать запись \U0001F4DD",
        callback_data="create_note")
    )
    builder.add(types.InlineKeyboardButton(
        text="Найти запись \U0001F50E",
        callback_data="find_note")
    )
    builder.add(types.InlineKeyboardButton(
        text="Посмотреть статистику \U0001F4CA",
        callback_data="view_statistics")
    )
    builder.add(types.InlineKeyboardButton(
        text="Добавить напоминание \U0001F4C6",
        callback_data="reminder")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )
    builder.add(types.InlineKeyboardButton(
        text="Помощь \U0001F91D",
        callback_data="help")
    )
    builder.adjust(2)

    await callback.message.answer(msg, reply_markup=builder.as_markup())



# Если не указать фильтр F.text, 
# то хэндлер сработает даже на картинку с подписью /test
@dp.message(F.text, Command("test"))
async def any_message(message: Message):
    await message.answer(
        "Hello, <b>world</b>!", 
        parse_mode=ParseMode.HTML
    )
    await message.answer(
        "Hello, *world*\!", 
        parse_mode=ParseMode.MARKDOWN_V2
    )

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer()
    # или просто await callback.answer()






# # Запуск процесса поллинга новых апдейтов
# async def main():
#     # while True:
#     #     # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
#     #     try:
#     #         await bot.polling(none_stop=True, interval=0)
#     #     # если возникла ошибка — сообщаем про исключение и продолжаем работу
#     #     except Exception as e: 
#     #         print('❌❌❌❌❌ Что-то пошло не так! ❌❌❌❌❌')
    
#     await dp.start_polling(bot)
from config_reader import config
# from handlers import common, ordering_food

async def main():
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    # )

    # # Если не указать storage, то по умолчанию всё равно будет MemoryStorage
    # # Но явное лучше неявного =]
    # dp = Dispatcher(storage=MemoryStorage())
    # bot = Bot(config.bot_token.get_secret_value())

    # dp.include_router(common.router)
    # dp.include_router(ordering_food.router)
    # # сюда импортируйте ваш собственный роутер для напитков

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())