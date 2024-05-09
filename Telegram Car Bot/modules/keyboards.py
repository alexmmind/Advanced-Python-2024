from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

start_bot_kbrd = [("Создать запись \U0001F4DD", 'create_note'), 
                    ("Найти запись \U0001F50E", 'find_note'), 
                    ("Посмотреть статистику \U0001F4CA", 'view_statistics'),
                    ("Добавить напоминание \U0001F4C6", 'reminder'),
                    ("На главную \U0001F3E0", 'start_bot'),
                    ("Помощь \U0001F91D", 'help')]

notes_type_kbdr = [("Заправка/расход \U000026FD", "fuel"),
                    ("Масло \U0001F6E2", "oil"),
                    ("Покупка запчастей \U00002699", "parts"),
                    ("Другая заметка \U0001F4DD", "other_note"),
                    ("На главную \U0001F3E0", "start_bot")]

find_type_kbrd = [("По теме \U00000023", "find_by_tag"),
                  ("По дате \U0001F4C5","find_by_date"),
                  ("По теме и дате \U0001F50E", "find_by_tag_and_date"),
                  ("На главную \U0001F3E0", "start_bot")]

find_tag_kbdr = [("Заправка/расход \U000026FD", "fuel_find"),
                    ("Масло \U0001F6E2", "oil_find"),
                    ("Покупка запчастей \U00002699", "parts_find"),
                    ("Другая заметка \U0001F4DD", "other_note_find"),
                    ("На главную \U0001F3E0", "start_bot")]

find_tag_kbdr_ = [("Заправка/расход \U000026FD", "fuel_find_"),
                    ("Масло \U0001F6E2", "oil_find_"),
                    ("Покупка запчастей \U00002699", "parts_find_"),
                    ("Другая заметка \U0001F4DD", "other_note_find_"),
                    ("На главную \U0001F3E0", "start_bot_")]

view_type_kbrd = [("По теме \U00000023", "view_by_tag"),
                  ("По дате \U0001F4C5", "view_by_date"),
                  ("По теме и дате \U0001F50E", "view_by_tag_and_date"),
                  ("На главную \U0001F3E0", "start_bot")]

oil_type_kbrd = [("Замена масла \U0001F504", "oil_change"),
                  ("Доливка масла \U00002935", "oil_refill"),
                  ("На главную \U0001F3E0", "start_bot")]

date_kbrd = [("Сегодняшняя дата \U0001F4C6", "today"),
                  ("Выбрать другую \U0001F4C5", "not_today")]

date_other_kbrd = [("Сегодняшняя дата \U0001F4C6", "today_other"),
                  ("Выбрать другую \U0001F4C5", "not_today_other")]

def get_yes_no_kbrd() -> ReplyKeyboardMarkup:
    kbrd = ReplyKeyboardBuilder()
    kbrd.button(text="Да")
    kbrd.button(text="Нет")
    kbrd.adjust(2)
    return kbrd.as_markup(resize_keyboard=True)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def make_inline_kbrd(items: "list[tuple]", row_width: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(InlineKeyboardButton(text=item[0], callback_data=item[1]))
    return builder.adjust(row_width)