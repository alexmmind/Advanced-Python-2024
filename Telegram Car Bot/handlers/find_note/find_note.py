from aiogram import types
import sys
sys.path.append("C:/Telegram Car Bot/modules/")
sys.path.append("C:/Telegram Car Bot/modules/keyboards.py")
# модуль работы со временем
import sqlite3 as sl
from aiogram import Router, F
from keyboards import make_inline_kbrd, find_type_kbrd, find_tag_kbdr_


from aiogram import Bot, types
from aiogram import F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sys
sys.path.append("C:/Telegram Car Bot/")
from aiogram.fsm.state import State, StatesGroup
from config_reader import config
from aiogram import Router, F
from modules.keyboards import make_inline_kbrd, start_bot_kbrd, find_tag_kbdr
from Data.data_pipeline import *
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
import pandas as pd


router = Router()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")
router = Router()

# find_type_kbrd = [("По тегу \U00000023", "find_by_tag"),
#                   ("По дате \U0001F4C5","find_by_date"),
#                   ("По тегу и дате \U0001F50E", "find_by_tag_and_date"),
#                   ("На главную \U0001F3E0", "start_bot")]

@router.callback_query(F.data == "find_note")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тип поиска",
        reply_markup=make_inline_kbrd(find_type_kbrd, 2).as_markup())


async def get_records_by_tag_(name, db_path, table_name, tag):
    """
    Возвращает все записи из sqlite3 таблицы, у которых тег в столбце "tag" соответствует заданному тегу.

    Args:
        db_path (str): Путь к базе данных.
        table_name (str): Название таблицы.
        tag (str): Заданный тег.

    Returns:
        list: Список записей, соответствующих заданному тегу.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Выполнение запроса
    # cursor.execute(f"SELECT * FROM {table_name} WHERE tag = ?", (tag,))
    cursor.execute(f"SELECT * FROM {table_name} WHERE tag = ? AND name = ?", (tag, name))

    # Возврат результатов
    records = cursor.fetchall()

    conn.close()

    return records


async def get_records_by_tag_as_df(name, db_path, table_name, col, tag):
    """
    Возвращает все записи из sqlite3 таблицы, у которых тег в столбце "tag" соответствует заданному тегу, в виде DataFrame pandas.

    Args:
        db_path (str): Путь к базе данных.
        table_name (str): Название таблицы.
        tag (str): Заданный тег.

    Returns:
        pd.DataFrame: DataFrame pandas с данными из таблицы.
    """ 
    try:

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Выполнение запроса
        # cursor.execute(f"SELECT * FROM {table_name} WHERE tag = ?", (tag,))
        cursor.execute(f"SELECT * FROM {table_name} WHERE {col} = ? AND name = ?", (tag, name))

        # Получение описания столбцов
        column_names = [column[0] for column in cursor.description]

        # Создание DataFrame
        df = pd.DataFrame(cursor.fetchall(), columns=column_names)
    finally:
        conn.close()
    return df

@router.callback_query(F.data == "find_by_tag")  
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тему поиска",
        reply_markup=make_inline_kbrd(find_tag_kbdr, 2).as_markup())
    # await state.set_state(FindNotes.mileage)


@router.callback_query(F.data == "fuel_find")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df(name, 'data.db', 'data', 'tag', 'fuel')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
пробег: {row['mileage']} км
количество литров: {row['litrage']} л
расход: {row['consumption']} л/100км.
\n''')
    
    await callback.message.answer(f"{''.join(formatted_rows)}", reply_markup=builder.as_markup())#,



@router.callback_query(F.data == "oil_find")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df(name, 'data.db', 'data', 'tag', 'oil')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
{row['type']}
пробег: {row['mileage']} км
количество литров: {row['litrage']} л
Бренд: {row['brand']}
Цена: {row['price']} руб.
\n''')
    
    await callback.message.answer(f"{''.join(formatted_rows)}", reply_markup=builder.as_markup())#,



@router.callback_query(F.data == "parts_find")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df(name, 'data.db', 'data', 'tag', 'parts')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
{row['text']}
\n''')
    
    await callback.message.answer(f"{''.join(formatted_rows)}", reply_markup=builder.as_markup())#,


@router.callback_query(F.data == "other_note_find")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df(name, 'data.db', 'data', 'tag', 'other')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
{row['text']}
\n''')
    
    await callback.message.answer(f"{''.join(formatted_rows)}", reply_markup=builder.as_markup())#,































class FindNotes(StatesGroup):
    date = State()
    date_tag = State()


@router.callback_query(F.data == "find_by_tag")  
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тему поиска",
        reply_markup=make_inline_kbrd(find_tag_kbdr, 2).as_markup())
    # await state.set_state(FindNotes.mileage)

@router.callback_query(F.data == "find_by_date")  
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    # date_str = date.strftime("%Y-%m-%d")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )
    await callback.message.answer(
        "Введите дату в формате Год-месяц-день, например 2024-01-01:",
        reply_markup=builder.as_markup())
    await state.set_state(FindNotes.date)


@router.message(FindNotes.date)
async def findDate(message: Message, state: FSMContext):
    bot_message_id = message.message_id - 1
    
    # Delete both messages
    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=message.from_user.username
    ans_ = "Ничего не найдено \U0001F625, попробуйте снова."
    try:
        # date_proc = datetime.strptime(message.text, "%Y-%m-%d")
        # date_proc = message.text.strftime("%Y-%m-%d")
        ans = await get_records_by_tag_as_df(name, 'data.db', 'data', 'date', message.text)    
        formatted_rows = []
        for index, row in ans.iterrows():
            if row['tag'] == 'oil':
                formatted_rows.append(f'''Дата: {row['date']}
Масло:
{row['type']}
пробег: {row['mileage']} км
количество литров: {row['litrage']} л
Бренд: {row['brand']}
Цена: {row['price']} руб.
\n''')
            if row['tag'] == 'fuel':
                formatted_rows.append(f'''Дата: {row['date']}
Заправка/расход:
пробег: {row['mileage']} км
количество литров: {row['litrage']} л
расход: {row['consumption']} л/100км.
\n''')
            if row['tag'] == 'parts':
                formatted_rows.append(f'''Дата: {row['date']}
Покупка запчастей:
{row['text']}
\n''')
            if row['tag'] == 'other':
                formatted_rows.append(f'''Дата: {row['date']}
Прочие заметки:
{row['text']}
\n''')
        ans_ = ''.join(formatted_rows)
        if len(formatted_rows) == 0:
            ans_ = "Ничего не найдено \U0001F625 попробуйте снова."
    except:
        ans_ = "Ничего не найдено \U0001F625 попробуйте снова."
    
    await message.answer(f"{ans_}", reply_markup=builder.as_markup())#,























async def get_records_by_tag_as_df_(name, db_path, table_name, col1, col2, date, tag):
    """
    Возвращает все записи из sqlite3 таблицы, у которых тег в столбце "tag" соответствует заданному тегу, в виде DataFrame pandas.

    Args:
        db_path (str): Путь к базе данных.
        table_name (str): Название таблицы.
        tag (str): Заданный тег.

    Returns:
        pd.DataFrame: DataFrame pandas с данными из таблицы.
    """ 
    try:

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Выполнение запроса
        # cursor.execute(f"SELECT * FROM {table_name} WHERE tag = ?", (tag,))
        cursor.execute(f"SELECT * FROM {table_name} WHERE {col1} = ? AND {col2} = ? AND name = ?", (date, tag, name))

        # Получение описания столбцов
        column_names = [column[0] for column in cursor.description]

        # Создание DataFrame
        df = pd.DataFrame(cursor.fetchall(), columns=column_names)
    finally:
        conn.close()
    return df


@router.callback_query(F.data == "find_by_tag_and_date")  
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    # date_str = date.strftime("%Y-%m-%d")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )
    await callback.message.answer(
        "Введите дату в формате Год-месяц-день, например 2024-01-01:",
        reply_markup=builder.as_markup())
    await state.set_state(FindNotes.date_tag)


@router.message(FindNotes.date_tag)
async def findDate(message: Message, state: FSMContext):
    bot_message_id = message.message_id - 1
    await state.update_data(date=message.text)
    
    # Delete both messages
    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)

    await message.answer(
        "Выберите тему поиска",
        reply_markup=make_inline_kbrd(find_tag_kbdr_, 2).as_markup())





@router.callback_query(F.data == "fuel_find_")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df_(name, 'data.db', 'data', 'date', 'tag', user_data['date'], 'fuel')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
пробег: {row['mileage']} км
количество литров: {row['litrage']} л
расход: {row['consumption']} л/100км.
\n''')
    ans_ = ''.join(formatted_rows)
    if len(formatted_rows) == 0:
        ans_ = "Ничего не найдено \U0001F625 попробуйте снова."
    
    await callback.message.answer(f"{ans_}", reply_markup=builder.as_markup())#,


@router.callback_query(F.data == "oil_find_")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df_(name, 'data.db', 'data', 'date', 'tag', user_data['date'], 'oil')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
{row['type']}
пробег: {row['mileage']} км
количество литров: {row['litrage']} л
Бренд: {row['brand']}
Цена: {row['price']} руб.
\n''')
    ans_ = ''.join(formatted_rows)
    if len(formatted_rows) == 0:
        ans_ = "Ничего не найдено \U0001F625 попробуйте снова."
    
    await callback.message.answer(f"{ans_}", reply_markup=builder.as_markup())#,


@router.callback_query(F.data == "parts_find_")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df_(name, 'data.db', 'data', 'date', 'tag', user_data['date'], 'parts')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
{row['text']}
\n''')
    ans_ = ''.join(formatted_rows)
    if len(formatted_rows) == 0:
        ans_ = "Ничего не найдено \U0001F625 попробуйте снова."
    
    await callback.message.answer(f"{ans_}", reply_markup=builder.as_markup())#,

@router.callback_query(F.data == "other_note_find_")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df_(name, 'data.db', 'data', 'date', 'tag', user_data['date'], 'other')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
{row['text']}
\n''')
    ans_ = ''.join(formatted_rows)
    if len(formatted_rows) == 0:
        ans_ = "Ничего не найдено \U0001F625 попробуйте снова."
    
    await callback.message.answer(f"{ans_}", reply_markup=builder.as_markup())#,


































































# @router.callback_query(F.data == "start_bot")   
# async def fuel(callback: types.CallbackQuery, state: FSMContext):
#     await state.clear()
#     await callback.message.delete()
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="Начать сначала \U000023EE",
#         callback_data="fuel")
#     )
#     builder.add(types.InlineKeyboardButton(
#         text="На главную \U0001F3E0",
#         callback_data="start_bot_fuel")
#     )
#     builder.adjust(2)
#     await callback.message.answer("Введите пробег:", reply_markup=builder.as_markup())#,
#     await state.set_state(FindNotes.mileage)

@router.callback_query(F.data == "start_bot_fuel")
async def save_fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())