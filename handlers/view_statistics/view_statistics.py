from aiogram import types
from aiogram import Router, F
import sys
import os
current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_directory)
from modules.config_reader import config
from modules.keyboards import *
from aiogram import Bot, types
from handlers.view_statistics import view_by_date_and_tag, view_by_tag

router = Router()
router.include_router(view_by_date_and_tag.router)
router.include_router(view_by_tag.router)

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")

@router.callback_query(F.data == "view_statistics")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тип фильтрации",
        reply_markup=make_inline_kbrd(view_type_kbrd, 2).as_markup())
