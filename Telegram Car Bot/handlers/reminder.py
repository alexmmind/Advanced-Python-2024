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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.callback_query(F.data == "reminder")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    # builder.add(types.InlineKeyboardButton(
    #     text=" По тегу \U00000023",
    #     callback_data="view_by_tag")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="По дате \U0001F4C5",
    #     callback_data="view_by_date")
    # )
    # builder.add(types.InlineKeyboardButton(
    #     text="По тегу и дате \U0001F50E",
    #     callback_data="view_by_tag_and_date")
    # )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )

    builder.adjust(1)
    await callback.message.answer(
        "Введите название напоминания:",
        reply_markup=builder.as_markup()
    )