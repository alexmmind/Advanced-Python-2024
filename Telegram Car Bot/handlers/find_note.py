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
import sys
sys.path.append("C:/Telegram Car Bot/modules/")
sys.path.append("C:/Telegram Car Bot/modules/keyboards.py")
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
from keyboards import make_inline_kbrd, start_bot_kbrd, notes_type_kbdr, find_type_kbrd, view_type_kbrd
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.callback_query(F.data == "find_note")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тип поиска",
        reply_markup=make_inline_kbrd(find_type_kbrd, 2).as_markup())