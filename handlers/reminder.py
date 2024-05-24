from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3 as sl
from aiogram import Router, F

from aiogram.types import FSInputFile

router = Router()
# @router.callback_query(F.data == "reminder")
# async def find_note(callback: types.CallbackQuery):
#     await callback.message.delete()
#     builder = InlineKeyboardBuilder()
#     # builder.add(types.InlineKeyboardButton(
#     #     text=" По тегу \U00000023",
#     #     callback_data="view_by_tag")
#     # )
#     # builder.add(types.InlineKeyboardButton(
#     #     text="По дате \U0001F4C5",
#     #     callback_data="view_by_date")
#     # )
#     # builder.add(types.InlineKeyboardButton(
#     #     text="По тегу и дате \U0001F50E",
#     #     callback_data="view_by_tag_and_date")
#     # )
#     builder.add(types.InlineKeyboardButton(
#         text="На главную \U0001F3E0",
#         callback_data="start_bot")
#     )

#     builder.adjust(1)
#     await callback.message.answer(
#         "Пока здесь ремонт, но скоро будет вкусно",
#         reply_markup=builder.as_markup()
#     )



@router.callback_query(F.data == "reminder")   
async def find_note(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot")
    )

    path = 'C:\\Telegram Car Bot\\Data\\soon.jpg'
    await callback.message.answer_photo(photo=FSInputFile(path, filename='Масло'), reply_markup=builder.as_markup()) #, caption='Ваши замены и доливки масла'