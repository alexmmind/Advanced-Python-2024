# import telebot
# from telebot import types
# import datetime
# import threading
# # from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
# bot = telebot.TeleBot('6515436458:AAGvkICeINuoeM7XELbtjqQw797k2ODsUHo')

# @bot.message_handler(commands=['start'])
# def welcome(message):
#     chat_id = message.chat.id
#     msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
#            " о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
#            " Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
#            " нажмите 'Старт' чтобы начать:")
    
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     button_help = telebot.types.InlineKeyboardButton(text="Старт \U0001F697",
#                                                      callback_data='start_bot')
#     keyboard.add(button_help)
#     bot.send_message(chat_id, msg, reply_markup=keyboard)

#         # bot.delete_message(call.message.chat.id, call.message.message_id)
#         # chat_id = message.chat.id
#         # keyboard = telebot.types.InlineKeyboardMarkup()
#         # button_help = telebot.types.InlineKeyboardButton(text="Помощь",
#         #                                                  callback_data='help')
#         # button_reminder = telebot.types.InlineKeyboardButton(text="Добавить напоминание",
#         #                                                  callback_data='reminder')
#         # keyboard.add(button_help, button_reminder)
#         # chat_id = message.chat.id
#         # keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#         # button_create = telebot.types.KeyboardButton(text="Создать запись")
#         # button_find = telebot.types.KeyboardButton(text="Найти запись")
#         # button_view = telebot.types.KeyboardButton(text="Посмотреть статистику")
#         # button_reminder = telebot.types.KeyboardButton(text="Добавить напоминание")
#         # button_help = telebot.types.KeyboardButton(text="Помощь")
#         # keyboard.add(button_create, button_find)
#         # keyboard.add(button_view, button_reminder)
#         # keyboard.add(button_help)
#     # bot.send_message(chat_id,
#     #                  'Добро пожаловать в бота - мобильного ассистента для вашего авто',
#     #                  reply_markup=keyboard)
    
# @bot.callback_query_handler(func=lambda call: call.data == 'start_bot')
# def save_btn(call):
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     message = call.message
#     chat_id = message.chat.id
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     button_create = telebot.types.InlineKeyboardButton(text="Создать запись \U0001F4DD",
#                                                      callback_data='create_note')
#     button_find = telebot.types.InlineKeyboardButton(text="Найти запись \U0001F50E",
#                                                      callback_data='find_note')
#     button_view = telebot.types.InlineKeyboardButton(text="Посмотреть статистику \U0001F4CA",
#                                                      callback_data='view')
#     button_reminder = telebot.types.InlineKeyboardButton(text="Добавить напоминание \U0001F4C6",
#                                                      callback_data='reminder')
#     button_home = telebot.types.InlineKeyboardButton(text="На главную \U0001F3E0",
#                                                      callback_data='start_bot')
#     button_help = telebot.types.InlineKeyboardButton(text="Помощь \U0001F91D",
#                                                      callback_data='help')
#     keyboard.add(button_create, button_find)
#     keyboard.add(button_view, button_reminder)
#     keyboard.add(button_help, button_home)
#     bot.send_message(chat_id,
#                      'Добро пожаловать в бота - мобильного ассистента для вашего авто',
#                      reply_markup=keyboard)
    

# @bot.callback_query_handler(func=lambda call: call.data == 'help')
# def save_btn(call):
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     message = call.message
#     chat_id = message.chat.id
#     msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
#            " о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
#            " Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
#            " нажмите 'Старт' чтобы начать:")
    
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     button_help = telebot.types.InlineKeyboardButton(text="Старт \U0001F697",
#                                                      callback_data='start_bot')
#     keyboard.add(button_help)
#     bot.send_message(chat_id, msg, reply_markup=keyboard)












# # Напоминания

# @bot.callback_query_handler(func=lambda call: call.data == 'reminder')
# def save_btn(call):
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     message = call.message
#     chat_id = message.chat.id
#     # bot.send_message(message.chat.id, 'Введите название напоминания:')
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     button_home = telebot.types.InlineKeyboardButton(text="Вернуться на главную \U0001F3E0",
#                                                      callback_data='start_bot')
#     keyboard.add(button_home)
#     bot.send_message(chat_id,
#                      'Введите название напоминания:',
#                      reply_markup=keyboard)
#     bot.register_next_step_handler(message, set_reminder_name)

# # @bot.message_handler(commands=['remove_keyboard'])
# # def remove_keyboard(message):
# #     chat_id = message.chat.id
# #     keyboard = telebot.types.ReplyKeyboardRemove()
# #     bot.send_message(chat_id,
# #                      'Удаляю клавиатуру',
# #                      reply_markup=keyboard)

# # @bot.message_handler(content_types='text')
# # def message_reply(message):
# #     chat_id = message.chat.id
# #     if message.text=="Добавить напоминание":
# #         keyboard = telebot.types.ReplyKeyboardRemove()
# #         bot.send_message(chat_id,
# #                      'Введите название напоминания:',
# #                      reply_markup=keyboard)
# #         # bot.send_message(message.chat.id, 'Введите название напоминания:')
# #         bot.register_next_step_handler(message, set_reminder_name)
# #     if message.text=="Помощь":
# #         msg = ("Вы находитесь в боте, цель которого помочь сохранить информацию"
# #                "о вашем авто. Он позволяет удобно хранить записи о расходе топлива, замене масел, расходников и т.д."
# #                "Также он позволяет добавить напоминания, например о смене масла или покупке запчастей."
# #                "нажмите /start чтобы начать")
# #         bot.send_message(message.chat.id, msg)

# # # Обработчик команды /reminder
# # @bot.message_handler(commands=['reminder'])
# # def reminder_message(message):
# # # Запрашиваем у пользователя название напоминания и дату и время напоминания
# #     bot.send_message(message.chat.id, 'Введите название напоминания:')
# #     bot.register_next_step_handler(message, set_reminder_name)






# # Функция, которую вызывает обработчик команды /reminder для установки названия напоминания
# def set_reminder_name(message):
#     bot.delete_message(message.chat.id, message.message_id)
#     user_data = {}
#     user_data[message.chat.id] = {'reminder_name': message.text}
#     bot.send_message(message.chat.id, 'Введите дату и время, когда вы хотите получить напоминание в формате ГГГГ-ММ-ДД чч:мм:сс.')
#     bot.register_next_step_handler(message, set_cal, user_data)

# @bot.callback_query_handler(func=lambda call: call.data == 'calendar')
# def set_cal(message):
#     calendar, step = DetailedTelegramCalendar().build()
#     bot.send_message(message.chat.id,
#                      f"Выбрать {LSTEP[step]}",
#                      reply_markup=calendar)
    
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
# def cal(call):
#     result, key, step = DetailedTelegramCalendar().process(call.data)
#     if not result and key:
#         bot.edit_message_text(f"Выбрать {LSTEP[step]}",
#                               call.message.chat.id,
#                               call.message.message_id,
#                               reply_markup=key)
#     elif result:
#         bot.edit_message_text(f"Вы выбрали {result}",
#                               call.message.chat.id,
#                               call.message.message_id)

# # Функция, которую вызывает обработчик команды /reminder для установки напоминания
# def reminder_set(message, user_data):
#     try:
#         # Преобразуем введенную пользователем дату и время в формат datetime
#         reminder_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M:%S')
#         now = datetime.datetime.now()
#         delta = reminder_time - now
#     # Если введенная пользователем дата и время уже прошли, выводим сообщение об ошибке
#         if delta.total_seconds() <= 0:
#             bot.send_message(message.chat.id, 'Вы ввели прошедшую дату, попробуйте еще раз.')
#         # Если пользователь ввел корректную дату и время, устанавливаем напоминание и запускаем таймер
#         else:
#             reminder_name = user_data[message.chat.id]['reminder_name']
#             bot.send_message(message.chat.id, 'Напоминание "{}" установлено на {}.'.format(reminder_name, reminder_time))
#             reminder_timer = threading.Timer(delta.total_seconds(), send_reminder, [message.chat.id, reminder_name])
#             reminder_timer.start()
#     # Если пользователь ввел некорректную дату и время, выводим сообщение об ошибке
#     except ValueError:
#         bot.send_message(message.chat.id, 'Вы ввели неверный формат даты и времени, попробуйте еще раз.')

# # Функция, которая отправляет напоминание пользователю
# def send_reminder(chat_id, reminder_name):
#     bot.send_message(chat_id, 'Время получить ваше напоминание "{}"!'.format(reminder_name))

# # Обработчик любого сообщения от пользователя
# @bot.message_handler(func=lambda message: True)
# def handle_all_message(message):
#     bot.send_message(message.chat.id, 'Я не понимаю, что вы говорите. Чтобы попасть в основное меню нажмите /start.')

# bot.polling(none_stop=True, interval=0)