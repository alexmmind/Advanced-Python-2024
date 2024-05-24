
from aiogram import types
from aiogram import Router, F
import sys
sys.path.append('C:\Telegram Car Bot\modules')
from keyboards import make_inline_kbrd, start_bot_kbrd, notes_type_kbdr, find_type_kbrd, view_type_kbrd, view_tag_kbdr_
# router = Router()


import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

from aiogram import types
import sys
sys.path.append("C:/Telegram Car Bot/modules/")
sys.path.append("C:/Telegram Car Bot/modules/keyboards.py")
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


@router.callback_query(F.data == "view_statistics")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тип фильтрации",
        reply_markup=make_inline_kbrd(view_type_kbrd, 2).as_markup())



async def get_records_by_tag_(name, db_path, table_name, tag):

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

async def df_stat(df, col_1, col_2):
    
    return df


@router.callback_query(F.data == "view_by_tag")  
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тему поиска",
        reply_markup=make_inline_kbrd(view_tag_kbdr_, 2).as_markup())
    # await state.set_state(FindNotes.mileage)

@router.callback_query(F.data == "start_bot_")
async def save_fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())

async def plot_col_2_over_time_and_save(df_, col_1, col_2, filename):
  df  = df_.copy()  
#   df[col_1] = df[col_1].apply(lambda x: datetime.fromtimestamp(float(x)))
  df[col_2] = df[col_2].apply(lambda x: float(x))

  plt.xlabel('Дата')
  plt.ylabel('Расход л/100км')

  plt.plot(df[col_1], df[col_2], marker='o', markerfacecolor='r', linestyle='-', color = 'b', linewidth = '1.7')
#   filepath = os.path.join(os.getcwd(), filename)
  plt.savefig(filename)
  plt.clf()
  return filename

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

async def plot_col_2_over_time_and_save_with_date(df_, col_1, col_2, filename):
  df  = df_.copy()  

  # Convert col_1 to datetime objects
  df[col_1] = pd.to_datetime(df[col_1])  

  df[col_2] = df[col_2].apply(lambda x: float(x))

  fig, ax = plt.subplots()

  plt.xlabel('Дата')
  plt.ylabel('Расход л/100км')

  ax.plot(df[col_1], df[col_2], marker='o', markerfacecolor='r', linestyle='-', color = 'b', linewidth = '1.7')
  ax.xaxis.set_major_locator(mdates.MonthLocator())
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
  plt.xticks(rotation=45)

  plt.tight_layout()
#   plt.show()
  plt.savefig(filename)
  plt.clf()
  return filename



from aiogram.types import FSInputFile
from aiogram.types import InputFile
@router.callback_query(F.data == "fuel_view_")   
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
    path = await plot_col_2_over_time_and_save_with_date(ans, 'date', 'consumption', 'C:\\Telegram Car Bot\\Data\\file.png') 
    path = 'C:\\Telegram Car Bot\\Data\\file.png'
    await callback.message.answer_photo(photo=FSInputFile(path, filename='Расход'), caption='График вашего расхода', reply_markup=builder.as_markup())
    # await bot.send_photo(callback.message.chat.id, photo=path, reply_markup=builder.as_markup())
    # await callback.message.answer(f"{''.join(formatted_rows)}", reply_markup=builder.as_markup())#,


import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from matplotlib.patches import Patch
from matplotlib.text import Text
import random

async def plot_oil(df_, col_1, col_2, filename, bar_width=0.0001):
    df = df_.copy()
    df[col_1] = df[col_1].apply(lambda x: datetime.fromtimestamp(float(x)))
    df[col_2] = df[col_2].apply(lambda x: float(x))

    # Set the x-axis label
    plt.xlabel('Дата')

    # Set the y-axis label
    plt.ylabel('Объем л.')

    # Create a bar chart of the data
    unique_types = df['type'].unique()
    color_map = {
        'Замена масла': 'blue',
        'Доливка масла': 'red',
    }

    # Assign random colors to any other types
    for type_ in unique_types:
        if type_ not in color_map:
            color_map[type_] = f'#{random.randint(0, 255):06x}'

    bars = plt.bar(df[col_1], df[col_2], color=[color_map[type_] for type_ in df['type']], width=bar_width)

    # Add value labels above each bar
    for bar in bars:
        height = bar.get_height()
        label_text = f'{height:.2f}'
        label_x = bar.get_x() + bar.get_width() / 2
        label_y = height + 0.02

        plt.text(label_x, label_y, label_text, ha='center', va='bottom')

    # Make the bars visible
    plt.ylim(bottom=0)  # Set the minimum y-axis value to 0

    # Create legend patches
    patches = [Patch(color=color_map[type_], label=type_) for type_ in unique_types]

    # Add a legend to the plot
    plt.legend(handles=patches, loc='upper right', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    # Save the plot to a file
    filepath = os.path.join(os.getcwd(), filename)
    plt.savefig(filename)
    plt.clf()

    # Show the plot (optional)
    # plt.show()

    return filename


from aiogram.types import FSInputFile
from aiogram.types import InputFile
@router.callback_query(F.data == "oil_view_")   
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
    path = await plot_oil(ans, 'id', 'litrage', 'C:\\Telegram Car Bot\\Data\\file.png') 
    path = 'C:\\Telegram Car Bot\\Data\\file.png'
    await callback.message.answer_photo(photo=FSInputFile(path, filename='Масло'), caption='Ваши замены и доливки масла', reply_markup=builder.as_markup())
    # await bot.send_photo(callback.message.chat.id, photo=path, reply_markup=builder.as_markup())
    # await callback.message.answer(f"{''.join(formatted_rows)}", reply_markup=builder.as_markup())#,


















class FindNotes(StatesGroup):
    date = State()
    date_tag = State()


# @router.callback_query(F.data == "find_by_tag")  
# async def fuel(callback: types.CallbackQuery, state: FSMContext):
#     # await state.clear()
#     await callback.message.delete()
#     await callback.message.answer(
#         "Выберите тему поиска",
#         reply_markup=make_inline_kbrd(find_tag_kbdr, 2).as_markup())
#     # await state.set_state(FindNotes.mileage)

@router.callback_query(F.data == "view_by_date")  
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


@router.callback_query(F.data == "view_by_tag_and_date")  
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

@router.callback_query(F.data == "start_bot_")
async def save_fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())