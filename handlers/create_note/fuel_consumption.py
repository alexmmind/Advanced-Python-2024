from aiogram import Bot, types
from aiogram import F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sys
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
import os
current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_directory)
from modules.config_reader import config
from modules.keyboards import *
from data.data_pipeline import *
router = Router()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")

#Fuel
##############################################################################################
class FuelConsumption(StatesGroup):
    mileage = State()
    litrage = State()

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

@router.callback_query(F.data == "fuel")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="fuel")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )
    builder.adjust(2)
    await callback.message.answer("Введите пробег:", reply_markup=builder.as_markup())#,
    await state.set_state(FuelConsumption.mileage)


@router.message(FuelConsumption.mileage)
async def kmSave(message: Message, state: FSMContext):
    bot_message_id = message.message_id - 1

    # Delete both messages
    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="fuel")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )
    builder.adjust(2)

    await state.update_data(mileage=float(message.text.lower().replace(",", ".")))
    # await callback.message.delete()
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите объем топлива:", reply_markup=builder.as_markup()
    )
    await state.set_state(FuelConsumption.litrage)

@router.message(FuelConsumption.litrage)
async def litrageSave(message: Message, state: FSMContext):
    bot_message_id = message.message_id - 1

    # Delete both messages
    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="fuel")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )
    builder.add(types.InlineKeyboardButton(
        text="Сохранить запись \U00002705",
        callback_data="save_fuel")
    )
    builder.adjust(2)

    await state.update_data(litrage=float(message.text.lower().replace(",", ".")))
    user_data = await state.get_data()
    await state.update_data(consumption=round(user_data['litrage']/user_data['mileage']*100, 2))
    user_data = await state.get_data()
    await message.answer(
        text=f"Ваш расход составил: {user_data['consumption']} л/100км", reply_markup=builder.as_markup()
    )

import datetime
@router.callback_query(F.data == "save_fuel")
async def save_fuel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(name=callback.from_user.username)
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_fuel")
    )

    ###
    #...
    now = datetime.datetime.now(datetime.timezone.utc)
    date = now.date()
    features_type = ['VARCHAR(40) PRIMARY KEY', #id
                     'VARCHAR(200)', #name
                     'VARCHAR(20)', #date
                     'VARCHAR(20)', #tag
                     'VARCHAR(500)', #consumption
                     'VARCHAR(500)', #litrage
                     'VARCHAR(500)'] #mileage
    
    data = ({"id": str(now.timestamp()), 
             "name": user_data["name"], 
             "date": str(date), 
             "tag": 'fuel',
             "consumption": user_data["consumption"], 
             "litrage": user_data["litrage"], 
             "mileage": user_data["mileage"]})
    await save_data(data, features_type)
    #...
    ###
    
    await callback.message.answer(
        text=f"Ваш расход составил: {user_data['consumption']} л/100км\nВсе данные сохранены", reply_markup=builder.as_markup()
    )

    await state.clear()

@router.callback_query(F.data == "start_bot_fuel")
async def save_fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())