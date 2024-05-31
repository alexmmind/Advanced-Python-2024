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
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from data.data_pipeline import *


router = Router()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")

class ViewNotes(StatesGroup):
    date_A = State()
    date_B = State()
    date_tag = State()


@router.callback_query(F.data == "view_by_date_and_tag")  
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    # date_str = date.strftime("%Y-%m-%d")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_view")
    )
    await callback.message.answer(
        "Введите начальную дату поиска в формате Год-месяц-день, например 2024-01-01:",
        reply_markup=builder.as_markup())
    await state.set_state(ViewNotes.date_A)

@router.message(ViewNotes.date_A)
async def kmSave(message: Message, state: FSMContext):
    bot_message_id = message.message_id - 1
    await message.delete()
    await state.update_data(date_A=message.text.lower())
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="view_by_date")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_view")
    )
    builder.adjust(2)
    await message.answer(
        "Введите конечную дату поиска в формате Год-месяц-день, например 2025-01-01:",
        reply_markup=builder.as_markup())
    await state.set_state(ViewNotes.date_B)


@router.message(ViewNotes.date_B)
async def findDate(message: Message, state: FSMContext):
    bot_message_id = message.message_id - 1
    await state.update_data(date_B=message.text)

    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)

    await message.answer(
        "Выберите тему поиска",
        reply_markup=make_inline_kbrd(view_tag_date_kbdr_, 2).as_markup())


@router.callback_query(F.data == "fuel_view")   
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
    ans = await get_records_by_tag_as_df_(name, config.DB_PATH, 'data', 'date', 'tag', user_data['date_A'], user_data['date_B'], 'fuel')    
    if ans.shape[0] == 0:
        await callback.message.answer(
            "Ничего не найдено \U0001F625 попробуйте снова.",
            reply_markup=builder.as_markup())
    path = await plot_fuel(ans, 'date', 'consumption', 'data\\file.png')
    await callback.message.answer_photo(photo=FSInputFile(path, filename='Расход'),
                                        caption='График вашего расхода',
                                        reply_markup=builder.as_markup())


@router.callback_query(F.data == "oil_view")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    # await state.clear()
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_view")
    )

    name=callback.from_user.username
    ans = await get_records_by_tag_as_df_(name, config.DB_PATH, 'data', 'date', 'tag', user_data['date_A'], user_data['date_B'], 'oil')  
    if ans.shape[0] == 0:
        await callback.message.answer(
            "Ничего не найдено \U0001F625 попробуйте снова.",
            reply_markup=builder.as_markup())
    path = await plot_oil(ans, 'date', 'litrage', 'data\\file.png') 
    await callback.message.answer_photo(photo=FSInputFile(path, filename='Масло'), 
                                        caption='Ваши замены и доливки масла', 
                                        reply_markup=builder.as_markup())



@router.callback_query(F.data == "start_bot_view")
async def start_oil(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())