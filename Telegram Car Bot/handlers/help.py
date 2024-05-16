from aiogram import types
import sqlite3 as sl
from aiogram import Router, F
import sys
sys.path.append("C:/Telegram Car Bot/modules/")
from keyboards import make_inline_kbrd, help_bot_kbrd

router = Router()
@router.callback_query(F.data == "help")
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
           " о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
           " Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
           "\n"
           "Вы можете создать заметку о своем автомобиле, содержащую информацию о расходе топлива, замене или доливке масла, покупке запчастей а также прочие заметки,"
           " также вы можете искать заметки по дате или их тегу, а также просматривать статистику по оставленным данным о вашем автомоибле."
           " Например график изменения расхода топлива.\n"
           "Воспользуйтесь одной из кнопок ниже, чтобы начать:")
    await callback.message.answer(msg, reply_markup=make_inline_kbrd(help_bot_kbrd, 2).as_markup())