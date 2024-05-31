import sys
import os
current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_directory)
from modules.config_reader import config
from modules.find_and_view_func import *
from modules.keyboards import *
from aiogram import Router, F, Bot, types
from aiogram.types import FSInputFile
from data.data_pipeline import *

router = Router()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")

@router.callback_query(F.data == "view_by_tag")  
async def fuel(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тему поиска",
        reply_markup=make_inline_kbrd(view_tag_kbdr_, 2).as_markup())

@router.callback_query(F.data == "fuel_view_")   
async def fuel(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )
    name=callback.from_user.username
    ans = await get_records_by_tag_as_df(name, config.DB_PATH, 'data', 'tag', 'fuel')   
    path = await plot_fuel(ans, 'date', 'consumption', 'data\\file.png')
    await callback.message.answer_photo(photo=FSInputFile(path, filename='Расход'),
                                        caption='График вашего расхода',
                                        reply_markup=builder.as_markup())

@router.callback_query(F.data == "oil_view_")   
async def fuel(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )
    name=callback.from_user.username
    ans = await get_records_by_tag_as_df(name, config.DB_PATH, 'data', 'tag', 'oil')   
    path = await plot_oil(ans, 'date', 'litrage', 'data\\file.png') 
    await callback.message.answer_photo(photo=FSInputFile(path, filename='Масло'), 
                                        caption='Ваши замены и доливки масла', 
                                        reply_markup=builder.as_markup())