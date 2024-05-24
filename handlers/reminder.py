from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3 as sl
from aiogram import Router, F

from aiogram.types import FSInputFile

router = Router()
@router.callback_query(F.data == "reminder")   
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )
    path = 'data\\soon.jpg'
    await callback.message.answer_photo(photo=FSInputFile(path, filename='Масло'), reply_markup=builder.as_markup()) #, caption='Ваши замены и доливки масла'