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
sys.path.append("C:/Telegram Car Bot/modules/")
from keyboards import make_inline_kbrd, start_bot_kbrd, notes_type_kbdr, find_type_kbrd, view_type_kbrd
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.callback_query(F.data == "help")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
           " о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
           " Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
           "\n"
           "Вы можете создать заметку о своем автомобиле, содержащую информацию о расходе топлива, замене или доливке масла, покупке запчастей а также прочие заметки,"
           " можете добавить напоминание на любую дату, например купить запчасть или поменять масло,"
           " также вы можете искать заметки по дате или их тегу, а также просматривать статистику по оставленным данным о вашем автомоибле."
           " Например средний расход топлива или график изменения расхода за год.\n"
           "Воспользуйтесь одной из кнопок ниже, чтобы начать:")
    await callback.message.answer(msg, reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())
