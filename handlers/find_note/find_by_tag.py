from aiogram.utils.keyboard import InlineKeyboardBuilder
import sys
import os
current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_directory)
from aiogram import Router, F, Bot, types
from modules.config_reader import config
from modules.find_and_view_func import *
from modules.keyboards import *
from aiogram.fsm.context import FSMContext
from data.data_pipeline import *

router = Router()

@router.callback_query(F.data == "find_by_tag")  
async def fuel(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тему поиска",
        reply_markup=make_inline_kbrd(find_tag_kbdr, 2).as_markup())

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
    ans = await get_records_by_tag_as_df(name, config.DB_PATH, 'data', 'tag', 'fuel')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
пробег: {row['mileage']} км
количество литров: {row['litrage']} л
расход: {row['consumption']} л/100км.
\n''')
    
    await callback.message.answer(f"{''.join(formatted_rows)}", reply_markup=builder.as_markup())#,

@router.callback_query(F.data == "oil_find")   
async def fuel(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df(name, config.DB_PATH, 'data', 'tag', 'oil')    
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
async def fuel(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df(name, config.DB_PATH, 'data', 'tag', 'parts')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
{row['text']}
\n''')
    
    await callback.message.answer(f"{''.join(formatted_rows)}", reply_markup=builder.as_markup())#,

@router.callback_query(F.data == "other_note_find")   
async def fuel(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df(name, config.DB_PATH, 'data', 'tag', 'other')    
    formatted_rows = []
    for index, row in ans.iterrows():
        formatted_rows.append(f'''Дата: {row['date']}
{row['text']}
\n''')
    await callback.message.answer(f"{''.join(formatted_rows)}", reply_markup=builder.as_markup())#,