from aiogram import types
import sys
from aiogram import Router, F
import os
current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_directory)
from modules.config_reader import config
from modules.keyboards import *
from data.data_pipeline import *
from handlers.create_note import fuel_consumption, oil_change, car_parts, other_notes

router = Router()
router.include_router(fuel_consumption.router)
router.include_router(oil_change.router)
router.include_router(car_parts.router)
router.include_router(other_notes.router)

@router.callback_query(F.data == "create_note")
async def create_note(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тип заметки",
        reply_markup=make_inline_kbrd(notes_type_kbdr, 2).as_markup())