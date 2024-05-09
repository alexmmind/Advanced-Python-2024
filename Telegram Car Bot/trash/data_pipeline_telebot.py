
import telebot
# модуль работы со временем
from datetime import datetime, timezone, timedelta
# модуль для работы с базой данных
import sqlite3 as sl

# указываем токен для доступа к боту
bot = telebot.TeleBot('6285051364:AAGG2iZ77NIeWj0YjqIs791qxPhvcS3Yu0s')

# приветственный текст
start_txt = 'Привет! Это журнал «Код». \n\nТеперь у бота появился бэкенд.'

# подключаемся к файлу с базой данных
con = sl.connect('reports.db')

# открываем файл
with con:
    # получаем количество таблиц с нужным нам именем
    data = con.execute("select count(*) from sqlite_master where type='table' and name='reports'")
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            # создаём таблицу для отчётов
            with con:
                con.execute("""
                    CREATE TABLE reports (
                        datetime VARCHAR(40) PRIMARY KEY,
                        date VARCHAR(20),
                        id VARCHAR(200),
                        name VARCHAR(200),
                        text VARCHAR(500)
                    );
                """)

# обрабатываем старт бота
@bot.message_handler(commands=['start'])
def start(message):
    # выводим приветственное сообщение
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')

# обрабатываем команду /now
@bot.message_handler(commands=['now'])
def start(message):
    # подключаемся к базе
    con = sl.connect('reports.db')   
    # получаем сегодняшнюю дату
    now = datetime.now(timezone.utc)
    date = now.date()
    # пустая строка для будущих отчётов
    s = ''
     # работаем с базой
    with con:
        # выполняем запрос к базе
        data = con.execute('SELECT * FROM reports WHERE date = :Date;',{'Date': str(date)})
        # перебираем все результаты
        for row in data:
            # формируем строку в общем отчёте
            s = s + '*' + row[3] + '*' + ' → ' + row[4] + '\n\n'
    # если отчётов не было за сегодня
    if s == '':
        # формируем новое сообщение
        s = 'За сегодня ещё нет записей'
    # отправляем общий отчёт обратно в телеграм
    bot.send_message(message.from_user.id, s, parse_mode='Markdown')

# обрабатываем команду /yesterday
@bot.message_handler(commands=['yesterday'])
def start(message):
    # подключаемся к базе
    con = sl.connect('reports.db')
    # получаем вчерашнюю дату
    yesterday = datetime.today() - timedelta(days=1)
    y_date = yesterday.date()
    # пустая строка для будущих отчётов
    s = ''
    # работаем с базой
    with con:
        # выполняем запрос
        data = con.execute('SELECT * FROM reports WHERE date = :Date;',{'Date': str(y_date)})
        # смотрим на результат
        for row in data:
            # если результат пустой — ничего не делаем
            if row[0] == 0:
                pass
            # если вчера были какие-то отчёты
            else:
                # добавляем их в общий список отчётов 
                s = s + '*' + row[3] + '*' + ' → ' + row[4] + '\n\n'
    # если отчётов не было за вчера
    if s == '':
        # формируем новое сообщение
        s = 'За вчерашний день нет записей'
    # отправляем пользователю это новое сообщение 
    bot.send_message(message.from_user.id, s, parse_mode='Markdown')

# обрабатываем входящий отчёт пользователя
@bot.message_handler(content_types=['text'])
def func(message):
    # подключаемся к базе
    con = sl.connect('reports.db')
    # подготавливаем запрос
    sql = 'INSERT INTO reports (datetime, date, id, name, text) values(?, ?, ?, ?, ?)'
    # получаем дату и время
    now = datetime.now(timezone.utc)
    # и просто дату
    date = now.date()
    # формируем данные для запроса
    data = [
        (str(now), str(date), str(message.from_user.id), str(message.from_user.username), str(message.text[:500]))
    ]
    # добавляем с помощью запроса данные
    with con:
        con.executemany(sql, data)
    # отправляем пользователю сообщение о том, что отчёт принят
    bot.send_message(message.from_user.id, 'Принято, спасибо!', parse_mode='Markdown')

# запускаем бота
if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e: 
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')