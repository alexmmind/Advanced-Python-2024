from aiogram import types
from aiogram.filters.command import Command
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3 as sl
from aiogram.filters import Command
from aiogram import Router, F

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