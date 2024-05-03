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

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
# from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
           " о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
           " Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
           " нажмите 'Старт' чтобы начать:")
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Старт \U0001F697",
        callback_data="start_bot"))
        
    await message.answer(msg, reply_markup=builder.as_markup())