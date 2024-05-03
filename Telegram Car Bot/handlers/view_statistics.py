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
import sys
sys.path.append('C:\Telegram Car Bot\modules')
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards import make_inline_kbrd, start_bot_kbrd, notes_type_kbdr, find_type_kbrd, view_type_kbrd
router = Router()

@router.callback_query(F.data == "view_statistics")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тип фильтрации",
        reply_markup=make_inline_kbrd(view_type_kbrd, 2).as_markup())