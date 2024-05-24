
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sys
from aiogram.fsm.state import State, StatesGroup
import os
current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_directory)
from aiogram import Router, F, Bot, types
from modules.keyboards import *
from modules.find_and_view_func import *
from modules.config_reader import config
from aiogram.fsm.context import FSMContext

router = Router()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")

class FindNotes(StatesGroup):
    date_A = State()
    date_B = State()
    date_tag = State()
    
@router.callback_query(F.data == "find_by_tag_and_date")  
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_find_TD")
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
        callback_data="find_by_tag_and_date")
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
    bot_message_id = message.message_id - 1
    await state.update_data(date_B=message.text)
    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)

    await message.answer(
        "Выберите тему поиска",
        reply_markup=make_inline_kbrd(find_tag_date_kbdr, 2).as_markup())


@router.callback_query(F.data == "fuel_find_")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_find_TD")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df_(name, config.DB_PATH, 'data', 'date', 'tag', user_data['date_A'], user_data['date_B'], 'fuel')   
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
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_find_TD")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df_(name, config.DB_PATH, 'data', 'date', 'tag', user_data['date_A'], user_data['date_B'], 'oil')   
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
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_find_TD")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df_(name, config.DB_PATH, 'data', 'date', 'tag', user_data['date_A'], user_data['date_B'], 'parts')   
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
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_find_TD")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df_(name, config.DB_PATH, 'data', 'date', 'tag', user_data['date_A'], user_data['date_B'], 'other')   
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
{row['text']}
\n''')
    ans_ = ''.join(formatted_rows)
    if len(formatted_rows) == 0:
        ans_ = "Ничего не найдено \U0001F625 попробуйте снова."
    
    await callback.message.answer(f"{ans_}", reply_markup=builder.as_markup())#,




@router.callback_query(F.data == "start_bot_find_TD")
async def save_fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())