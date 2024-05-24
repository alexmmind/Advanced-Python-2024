from aiogram import types
import sys

from aiogram import Router, F
import sys
import os
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_directory)
from modules.keyboards import make_inline_kbrd, start_bot_kbrd


router = Router()

@router.callback_query(F.data == "start_bot")
async def start_bot(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())