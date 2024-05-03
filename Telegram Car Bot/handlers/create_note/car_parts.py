from aiogram import Bot, types
from aiogram import F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sys
import datetime
sys.path.append("C:/Telegram Car Bot/")
sys.path.append("C:/Telegram Car Bot/modules/")
from modules.datetime_converter import convert_date_to_datetime
from aiogram.fsm.state import State, StatesGroup
from config_reader import config
from aiogram import Router, F
from modules.keyboards import make_inline_kbrd, start_bot_kbrd, date_kbrd
from aiogram.fsm.context import FSMContext
router = Router()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")


class PurchaseParts(StatesGroup):
    text = State()
    date = State()

@router.callback_query(F.data == "parts")
async def create_note(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Создать запись с сегодняшней датой или выбрать другую?",
        reply_markup=make_inline_kbrd(date_kbrd, 2).as_markup())


###############################################################################
@router.callback_query(F.data == "today")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    today = datetime.date.today()
    await state.update_data(date=today.strftime("%d-%m-%Y"))

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="parts")
    )

    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_parts")
    )
    builder.adjust(2)
    await callback.message.answer("Введите что вы купили в свободной форме:", reply_markup=builder.as_markup())#,
    await state.set_state(PurchaseParts.text)


@router.callback_query(F.data == "not_today")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    today = datetime.date.today()
    await state.update_data(type=today)#.strftime("%d-%m-%Y"))

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="parts")
    )

    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_parts")
    )
    builder.adjust(2)
    await callback.message.answer("Введите дату в форме день-месяц-год:", reply_markup=builder.as_markup())#,
    await state.set_state(PurchaseParts.date)
  
@router.message(PurchaseParts.date)
async def kmSave(message: Message, state: FSMContext):
    bot_message_id = message.message_id - 1

    await message.delete()
    await state.update_data(date=convert_date_to_datetime(message.text.lower()))
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="parts")
    )

    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_parts")
    )
    builder.adjust(2)

    await message.answer("Введите что вы купили в свободной форме:", reply_markup=builder.as_markup())#,
    await state.set_state(PurchaseParts.text)


@router.message(PurchaseParts.text)
async def litrageSave(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    bot_message_id = message.message_id - 1

    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="parts")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_parts")
    )
    builder.add(types.InlineKeyboardButton(
        text="Сохранить запись \U00002705",
        callback_data="save_parts")
    )
    builder.adjust(2)

    user_data = await state.get_data()
    await message.answer(
        text=f'''Вы ввели:\nДата: {user_data['date']}\nПокупка:\n{user_data['text']}''', reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "save_parts")
async def save_oil(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную  \U0001F3E0",
        callback_data="start_bot_parts")
    )

    ###
    #...
    #Работа с БД
    #...
    ###
    
    await callback.message.answer(
        text=f'''Сохраненная запись:\nДата: {user_data['date']}\nПокупка:\n{user_data['text']}''', reply_markup=builder.as_markup()
    )
    await state.clear()

@router.callback_query(F.data == "start_bot_parts")
async def start_oil(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())