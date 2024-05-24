import sqlite3 as sl #бд
import datetime
from datetime import timezone
import sqlite3


async def save_data(data, features_type):

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    features_str = ", ".join([f"{key} {type_}" for key, type_ in zip(data.keys(), features_type)])
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS data ({features_str})''') 
    ind = 0
    for col in data.keys():
        cursor.execute(f"SELECT name FROM pragma_table_info('data') WHERE name='{col}'")
        column_exists = cursor.fetchone()
        if not column_exists:
            cursor.execute(f"ALTER TABLE data ADD COLUMN {col} {features_type[ind]}")
        ind += 1
    try:
        column = ", ".join([f"{key}" for key in data.keys()])
        placeholders = ','.join('?' * len(data))
        cursor.execute(f"INSERT INTO data ({column}) VALUES ({placeholders})", list(data.values()))
        conn.commit()
        return True
    except sqlite3.Error as error:
        print("Error saving data:", error)
        return False
    finally:
        conn.close()


async def save_oil(user_data):
    # # подключаемся к файлу с базой данных
    con = sl.connect('database.db')

    # открываем файл
    with con:
        # получаем количество таблиц с нужным нам именем
        data = con.execute("select count(*) from sqlite_master where type='table' and name='database'")
        for row in data:
            # если таких таблиц нет
            if row[0] == 0:
                # создаём таблицу для отчётов
                with con:
                    con.execute("""
                        CREATE TABLE database (
                            datetime VARCHAR(40) PRIMARY KEY,
                            date VARCHAR(20),
                            id VARCHAR(200),
                            name VARCHAR(200),
                            type VARCHAR(500),
                            mileage VARCHAR(500),
                            litrage VARCHAR(500),
                            brand VARCHAR(1500),
                            price VARCHAR(500),
                        );
                    """)
    # подключаемся к базе

    # подготавливаем запрос
    sql = 'INSERT INTO database (datetime, date, id, name, type, mileage, litrage, brand, price) values(?, ?, ?, ?, ?, ?, ?, ?, ?)'
    # получаем дату и время
    now = datetime.now(timezone.utc)
    # и просто дату
    date = now.date()

    # формируем данные для запроса
    data = [
        (str(now), str(date), str(user_data['id']), str(user_data['usrname']),
         str(user_data['type']), float(user_data['mileage'], float(user_data['litrage']), 
                                       str(user_data['brand']), str(user_data['price'])))
    ]
    # добавляем с помощью запроса данные
    with con:
        con.executemany(sql, data)




async def save_oil_change_data(data):


    # Connect to the database (create a new one if it doesn't exist)
    conn = sqlite3.connect("oil_change_data.db")

    # Create a cursor object
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS oil_change_data (
            datetime VARCHAR(40) PRIMARY KEY,
            id VARCHAR(200),
            name VARCHAR(200),
            date VARCHAR(20),
            type VARCHAR(500),
            mileage VARCHAR(500),
            litrage VARCHAR(500),
            brand VARCHAR(1500),
            price VARCHAR(500)
        )
    """)

    # Insert the data into the table
    try:    # получаем дату и время
        now = datetime.datetime.now(datetime.timezone.utc)
        # и просто дату
        date = now.date()
        cursor.execute("""
            INSERT INTO oil_change_data (
                id,
                name,
                date,
                type,
                mileage,
                litrage,
                brand,
                price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, 
        # (str(now), str(date), data["id"], data["name"], data["type"], data["mileage"], data["litrage"], data["brand"], data["price"]))

        (str(now.timestamp()), data["name"], str(date), data["type"], data["mileage"], data["litrage"], data["brand"], data["price"]))
        conn.commit()
        return True
    except sqlite3.Error as error:
        print("Error saving data:", error)
        return False

    # Close the database connection
    finally:
        conn.close()


async def save_data_(data, features_type):

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    # keys = ", ".join(data.keys())
    features_str = ", ".join([f"{key} {type_}" for key, type_ in zip(data.keys(), features_type)])
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS data ({features_str})''') 
    try:    # получаем дату и время
        # cursor.execute(f'''INSERT INTO data ({keys}) VALUES ([{'?, '*len(features_type)}])''', data)
        column = ", ".join([f":{key}" for key in data.keys()])
        cursor.executemany(f"INSERT INTO data VALUES({column})", data)
        # column = ", ".join([f":{key}" for key in data.keys()])
        # cursor.executemany(f"INSERT INTO data ({keys}) VALUES ({column})", data)
        # (str(now), str(date), data["id"], data["name"], data["type"], data["mileage"], data["litrage"], data["brand"], data["price"]))
        # (str(now.timestamp()), data["name"], str(date), data["type"], data["mileage"], data["litrage"], data["brand"], data["price"]))
        conn.commit()
        return True
    except sqlite3.Error as error:
        print("Error saving data:", error)
        return False
    # Close the database connection
    finally:
        conn.close()

