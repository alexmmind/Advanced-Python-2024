from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
import sys
import os
current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_directory)
from aiogram import Router, F, Bot, types
from modules.keyboards import *
from modules.find_and_view_func import *
from modules.config_reader import config
from aiogram.fsm.context import FSMContext
from data.data_pipeline import *


router = Router()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")

class FindNotes(StatesGroup):
    date_A = State()
    date_B = State()
    date_tag = State()


@router.callback_query(F.data == "find_by_date") 
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )
    await callback.message.answer(
        "Введите начальную дату поиска в формате Год-месяц-день, например 2024-01-01:",
        reply_markup=builder.as_markup())
    await state.set_state(FindNotes.date_A)


@router.message(FindNotes.date_A)
async def kmSave(message: Message, state: FSMContext):
    bot_message_id = message.message_id - 1
    await message.delete()
    await state.update_data(date_A=message.text.lower())
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="find_by_date")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_find_TD")
    )
    builder.adjust(2)
    await message.answer(
        "Введите конечную дату поиска в формате Год-месяц-день, например 2025-01-01:",
        reply_markup=builder.as_markup())
    await state.set_state(FindNotes.date_B)


@router.message(FindNotes.date_B)
async def findDate(message: Message, state: FSMContext):
    await state.update_data(date_B=message.text)
    bot_message_id = message.message_id - 1
    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=message.from_user.username
    user_data = await state.get_data()
    ans_ = "Ничего не найдено \U0001F625, попробуйте снова."
    try:
        ans = await get_records_by_date(name, config.DB_PATH, 'data', 'date', 'tag', user_data['date_A'], user_data['date_B'])
        print(ans.shape)
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





@router.callback_query(F.data == "start_bot_fuel")
async def save_fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())