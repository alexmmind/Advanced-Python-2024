##################################################################
# Предыдущая версия бота без вырезанного кода находится в /trash/bot_rezerv.py
##################################################################

import sys
sys.path.append('C:\Telegram Car Bot\modules')
import asyncio
import logging
from config_reader import config
from aiogram import Bot, Dispatcher
from handlers import find_note, help, start, start_bot, view_statistics, reminder
from handlers.create_note import create_note


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")
    dp = Dispatcher()
    dp.include_routers(start.router, start_bot.router, help.router, create_note.router, find_note.router, view_statistics.router, reminder.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())