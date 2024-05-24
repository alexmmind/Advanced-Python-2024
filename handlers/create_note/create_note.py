from aiogram import types
import sys
sys.path.append("C:/Telegram Car Bot/")
sys.path.append("C:/Telegram Car Bot/handlers/")
from aiogram import Router, F
sys.path.append("C:/Telegram Car Bot/handlers/create_note/")
from modules.keyboards import make_inline_kbrd, notes_type_kbdr
import fuel_consumption, oil_change, car_parts, other_notes

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