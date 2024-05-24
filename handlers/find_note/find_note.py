import sys
import os
current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_directory)
from modules.config_reader import config
from modules.keyboards import *
from modules.find_and_view_func import *
from aiogram import Router, F, Bot, types
from handlers.find_note import find_by_tag, find_by_date, find_by_date_and_tag

router = Router()
router.include_router(find_by_tag.router)
router.include_router(find_by_date.router)
router.include_router(find_by_date_and_tag.router)

@router.callback_query(F.data == "find_note")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тип поиска",
        reply_markup=make_inline_kbrd(find_type_kbrd, 2).as_markup())