import logging
import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '6515436458:AAGvkICeINuoeM7XELbtjqQw797k2ODsUHo'  # Replace with your API token
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config_reader import config
from random import randint

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Для записей с типом Secret* необходимо 
# вызывать метод get_secret_value(), 
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()

@dp.message(commands=['start'])
async def welcome(message: types.Message):
   chat_id = message.chat.id
   msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
          " о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
          " Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
          " нажмите 'Старт' чтобы начать:")
   
   keyboard = InlineKeyboardMarkup()
   button_help = InlineKeyboardButton(text="Старт \U0001F697", callback_data='start_bot')
   keyboard.add(button_help)
   await bot.send_message(chat_id, msg, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == 'start_bot')
async def save_btn(call: types.CallbackQuery):
   await bot.delete_message(call.message.chat.id, call.message.message_id)
   message = call.message
   chat_id = message.chat.id
   keyboard = InlineKeyboardMarkup()
   button_create = InlineKeyboardButton(text="Создать запись \U0001F4DD", callback_data='create_note')
   button_find = InlineKeyboardButton(text="Найти запись \U0001F50E", callback_data='find_note')
   button_view = InlineKeyboardButton(text="Посмотреть статистику \U0001F4CA", callback_data='view')
   button_reminder = InlineKeyboardButton(text="Добавить напоминание \U0001F4C6", callback_data='reminder')
   button_home = InlineKeyboardButton(text="На главную \U0001F3E0", callback_data='start_bot')
   button_help = InlineKeyboardButton(text="Помощь \U0001F91D", callback_data='help')
   keyboard.add(button_create, button_find)
   keyboard.add(button_view, button_reminder)
   keyboard.add(button_help, button_home)
   await bot.send_message(chat_id, 'Добро пожаловать в бота - мобильного ассистента для вашего авто', reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == 'help')
async def save_btn(call: types.CallbackQuery):
   await bot.delete_message(call.message.chat.id, call.message.message_id)
   message = call.message
   chat_id = message.chat.id
   msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
          " о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
          " Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
          " нажмите 'Старт' чтобы начать:")
   
   keyboard = InlineKeyboardMarkup()
   button_help = InlineKeyboardButton(text="Старт \U0001F697", callback_data='start_bot')
   keyboard.add(button_help)
   await bot.send_message(chat_id, msg, reply_markup=keyboard)

# More handlers for reminders, calendars, and other functionality can be added similarly

if __name__ == '__main__':
   # Start long-polling mode
   executor = dp.start_polling(dp, skip_updates=True)
   asyncio.get_event_loop().run_until_complete(executor)
