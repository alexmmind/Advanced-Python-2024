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
import sys
sys.path.append("C:/Telegram Car Bot/")
sys.path.append("C:/Telegram Car Bot/handlers/")
from random import randint
from aiogram.filters import Command
from aiogram.utils.formatting import Text, Bold
# import telebot
# модуль работы со временем
from datetime import datetime, timezone, timedelta
# модуль для работы с базой данных
import sqlite3 as sl
from aiogram.filters import Command, StateFilter
# from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiogram.dispatcher
# from aiogram.dispatcher import FSMContext
import asyncio
import logging
# from bot import bot
from config_reader import config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
# from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from start_bot import start_bot
sys.path.append("C:/Telegram Car Bot/handlers/create_note/")
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from modules.keyboards import make_inline_kbrd, start_bot_kbrd, notes_type_kbdr, find_type_kbrd, view_type_kbrd
import fuel_consumption

router = Router()

router.include_router(fuel_consumption.router)
@router.callback_query(F.data == "create_note")
async def create_note(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тип заметки",
        reply_markup=make_inline_kbrd(notes_type_kbdr, 2).as_markup())

#Fuel
##############################################################################################
# class FuelConsumption(StatesGroup):
#     mileage = State()
#     litrage = State()

# from aiogram.filters import Command, StateFilter
# from aiogram.fsm.context import FSMContext

# @router.callback_query(F.data == "fuel")   
# async def fuel(callback: types.CallbackQuery, state: FSMContext):
#     await state.clear()
#     await callback.message.delete()
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="Начать сначала",
#         callback_data="fuel")
#     )
#     builder.add(types.InlineKeyboardButton(
#         text="На главную",
#         callback_data="start_bot_fuel")
#     )
#     builder.adjust(2)
#     await callback.message.answer("Введите пробег:", reply_markup=builder.as_markup())#,
#     await state.set_state(FuelConsumption.mileage)


# @router.message(FuelConsumption.mileage)
# async def kmSave(message: Message, state: FSMContext):
#     bot_message_id = message.message_id - 1

#     # Delete both messages
#     await message.delete()
#     await bot.delete_message(message.chat.id, bot_message_id)
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="Начать сначала",
#         callback_data="fuel")
#     )
#     builder.add(types.InlineKeyboardButton(
#         text="На главную",
#         callback_data="start_bot_fuel")
#     )
#     builder.adjust(2)

#     await state.update_data(km=float(message.text.lower().replace(",", ".")))
#     # await callback.message.delete()
#     await message.answer(
#         text="Спасибо. Теперь, пожалуйста, введите объем топлива:", reply_markup=builder.as_markup()
#     )
#     await state.set_state(FuelConsumption.litrage)

# @router.message(FuelConsumption.litrage)
# async def litrageSave(message: Message, state: FSMContext):
#     bot_message_id = message.message_id - 1

#     # Delete both messages
#     await message.delete()
#     await bot.delete_message(message.chat.id, bot_message_id)
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="Исправить ошибки и начать сначала",
#         callback_data="fuel")
#     )
#     builder.add(types.InlineKeyboardButton(
#         text="На главную",
#         callback_data="start_bot_fuel")
#     )
#     builder.add(types.InlineKeyboardButton(
#         text="Сохранить запись",
#         callback_data="save_fuel")
#     )
#     builder.adjust(2)

#     await state.update_data(liters=float(message.text.lower().replace(",", ".")))
#     user_data = await state.get_data()
#     await state.update_data(consumption=round(user_data['liters']/user_data['km']*100, 2))
#     user_data = await state.get_data()
#     await message.answer(
#         text=f"Ваш расход составил: {user_data['consumption']} л/100км", reply_markup=builder.as_markup()
#     )

# @router.callback_query(F.data == "save_fuel")
# async def save_fuel(callback: types.CallbackQuery, state: FSMContext):
#     await callback.message.delete()
#     user_data = await state.get_data()
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="На глвавную",
#         callback_data="start_bot")
#     )

#     ###
#     #...
#     #Работа с БД
#     #...
#     ###
    
#     await callback.message.answer(
#         text=f"Ваш расход составил: {user_data['consumption']} л/100км\nВсе данные сохранены", reply_markup=builder.as_markup()
#     )

#     await state.clear()

# @router.callback_query(F.data == "start_bot_fuel")
# async def save_fuel(callback: types.CallbackQuery, state: FSMContext):
#     await state.clear()
#     await callback.message.delete()
#     await callback.message.answer(
#         "Добро пожаловать в бота - мобильного ассистента для вашего авто",
#         reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())