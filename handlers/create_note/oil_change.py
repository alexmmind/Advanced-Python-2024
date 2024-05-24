from aiogram import Bot, types
from aiogram import F
from aiogram.types import Message
import datetime
from datetime import timezone
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sys
import os
current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_directory)
from modules.config_reader import config
from modules.keyboards import *
from data.data_pipeline import *
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
router = Router()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="None")


class OilChange(StatesGroup):
    mileage = State()
    litrage = State()
    price = State()
    brand = State()
    oil_type = State()

@router.callback_query(F.data == "oil")
async def create_note(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Выберите тип заметки",
        reply_markup=make_inline_kbrd(oil_type_kbrd, 2).as_markup())
    


@router.callback_query(F.data == "oil_change")   
async def fuel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.adjust(2)
    await state.update_data(type='Замена масла')
    await callback.message.answer("Введите пробег:", reply_markup=builder.as_markup())#,
    await state.set_state(OilChange.mileage)



@router.callback_query(F.data == "oil_refill")   
async def oil_refill(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.adjust(2)
    await state.update_data(type='Доливка масла')
    await callback.message.answer("Введите пробег:", reply_markup=builder.as_markup())#,
    await state.set_state(OilChange.mileage)



@router.message(OilChange.mileage)
async def kmSave(message: Message, state: FSMContext):
    bot_message_id = message.message_id - 1

    await message.delete()
    await state.update_data(mileage=message.text.lower())
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.adjust(2)

    await state.update_data(km=float(message.text.lower().replace(",", ".")))
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите объем масла:", reply_markup=builder.as_markup()
    )
    await state.set_state(OilChange.litrage)



@router.message(OilChange.litrage)
async def litrageSave(message: Message, state: FSMContext):
    await state.update_data(litrage=message.text.lower())
    bot_message_id = message.message_id - 1
    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="Пропустить \U0000274C",
        callback_data="skip_brand")
    )
    builder.adjust(2)

    await message.answer(
        text=f"Укажите бренд и марку масла, по желанию\nЕсли вы хотите пропустить этот пункт, нажмите кнопку 'Пропустить'", reply_markup=builder.as_markup()
    )
    await state.set_state(OilChange.brand)



@router.callback_query(F.data == "skip_brand")
async def skip_brand(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Цена за литр \U0001F4B5",
        callback_data="oil_l_price")
    )
    builder.add(types.InlineKeyboardButton(
        text="Полная цена \U0001F4B8",
        callback_data="oil_full_price")
    )
    builder.add(types.InlineKeyboardButton(
        text="Пропустить \U0000274C",
        callback_data="skip_price")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.adjust(2)
    await callback.message.answer(
        text=f"Выбирете формат цены за масло\nЕсли вы хотите пропустить этот пункт, нажмите кнопку 'Пропустить'", reply_markup=builder.as_markup()
    )
    await state.update_data(brand="(Нет данных)")
    await state.set_state(OilChange.price)



@router.message(OilChange.brand)
async def kmSave(message: Message, state: FSMContext):
    await state.update_data(brand=message.text.lower())
    bot_message_id = message.message_id - 1

    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Цена за литр \U0001F4B5",
        callback_data="oil_l_price")
    )
    builder.add(types.InlineKeyboardButton(
        text="Полная цена \U0001F4B8",
        callback_data="oil_full_price")
    )
    builder.add(types.InlineKeyboardButton(
        text="Пропустить \U0000274C",
        callback_data="skip_price")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.adjust(2)
    await message.answer(
        text=f"Выбирете формат цены за масло\nЕсли вы хотите пропустить этот пункт, нажмите кнопку 'Пропустить'", reply_markup=builder.as_markup()
    )
    await state.set_state(OilChange.price)



@router.callback_query(F.data == "skip_price")
async def skip_price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="Сохранить запись \U00002705",
        callback_data="save_oil")
    )
    builder.adjust(2)
    await state.update_data(price="(Нет данных)")


    user_data = await state.get_data()
    await callback.message.answer(
        text=f'''Сохраненная запись:\n{user_data['type']}\nПробег: {user_data['mileage']} км\nОбъем: {user_data['litrage']} л\nБренд: {user_data['brand']}\nЦена: {user_data['price']} руб.''', reply_markup=builder.as_markup()
    )



@router.callback_query(F.data == "oil_l_price")
async def oil_LP(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.adjust(2)
    await callback.message.answer(
        text=f"Укажите цену:", reply_markup=builder.as_markup()
    )
    await state.set_state(OilChange.price)
    


@router.callback_query(F.data == "oil_full_price")
async def oil_FP(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.adjust(2)

    await callback.message.answer(
        text=f"Укажите цену:", reply_markup=builder.as_markup()
    )
    await state.set_state(OilChange.price)



@router.message(OilChange.price)
async def litrageSave(message: Message, state: FSMContext):
    await state.update_data(price=message.text.lower())
    bot_message_id = message.message_id - 1

    await message.delete()
    await bot.delete_message(message.chat.id, bot_message_id)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать сначала \U000023EE",
        callback_data="oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )
    builder.add(types.InlineKeyboardButton(
        text="Сохранить запись \U00002705",
        callback_data="save_oil")
    )
    builder.adjust(2)


    user_data = await state.get_data()
    await message.answer(
        text=f'''Вы ввели:\n{user_data['type']}\nПробег: {user_data['mileage']} км\nОбъем: {user_data['litrage']} л\nБренд: {user_data['brand']}\nЦена: {user_data['price']} руб.''', reply_markup=builder.as_markup()
    )



@router.callback_query(F.data == "save_oil")
async def save_oil(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(name=callback.from_user.username)
    # await state.update_data(id=callback.message.message_id)
    await state.update_data(name=callback.from_user.username)
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="На главную \U0001F3E0",
        callback_data="start_bot_oil")
    )

    ###
    #...
    #Работа с БД
    # await save_oil(user_data, state)
    now = datetime.datetime.now(datetime.timezone.utc)
    # и просто дату
    date = now.date()
    features_type = ['VARCHAR(40) PRIMARY KEY', #id
                     'VARCHAR(200)', #name
                     'VARCHAR(20)',  #date
                     'VARCHAR(20)',  #tags
                     'VARCHAR(500)', #type
                     'VARCHAR(500)', #mileage
                     'VARCHAR(500)', #litrage
                     'VARCHAR(1500)', #brand
                     'VARCHAR(500)'] #price
    
    data = ({"id": str(now.timestamp()), 
             "name": user_data["name"], 
             "date": str(date), 
             "tag": 'oil',
             "type": user_data["type"], 
             "mileage": user_data["mileage"], 
             "litrage": user_data["litrage"], 
             "brand": user_data["brand"], 
             "price": user_data["price"]})
    await save_data(data, features_type)
    #...
    ###
    
    await callback.message.answer(
        text=f'''Сохраненная запись:\n{user_data['type']}\nПробег: {user_data['mileage']} км\nОбъем: {user_data['litrage']} л\nБренд: {user_data['brand']}\nЦена: {user_data['price']} руб.''', reply_markup=builder.as_markup()
    )

    await state.clear()



@router.callback_query(F.data == "start_bot_oil")
async def start_oil(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Добро пожаловать в бота - мобильного ассистента для вашего авто",
        reply_markup=make_inline_kbrd(start_bot_kbrd, 2).as_markup())