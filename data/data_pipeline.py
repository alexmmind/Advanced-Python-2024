import sqlite3
import sys
import os
import pandas as pd


current_dir = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_directory)
from modules.config_reader import config


async def save_data(data, features_type):
    conn = sqlite3.connect(config.DB_PATH)
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


async def get_records_by_tag_(name, db_path, table_name, tag):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE tag = ? AND name = ?", (tag, name))
    records = cursor.fetchall()
    conn.close()
    return records



async def get_records_by_tag_as_df(name, db_path, table_name, col, tag):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE {col} = ? AND name = ?", (tag, name))
        column_names = [column[0] for column in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=column_names)
    finally:
        conn.close()
    return df



async def get_records_by_tag_as_df_(name, db_path, table_name, col1, col2, date, tag):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE {col1} = ? AND {col2} = ? AND name = ?", (date, tag, name))
        column_names = [column[0] for column in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=column_names)
    finally:
        conn.close()
    return df



async def get_records_by_tag_and_date_as_df(name, db_path, table_name, col1, col2, date, tag):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE {col1} = ? AND {col2} = ? AND name = ?", (date, tag, name))
        column_names = [column[0] for column in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=column_names)
    finally:
        conn.close()
    return df



async def get_records_by_tag_as_df_(name, db_path, table_name, col1, col2, date_A, date_B, tag):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        query = f"SELECT * FROM {table_name} WHERE {col1} BETWEEN ? AND ? AND {col2} = ? AND name = ?"
        cursor.execute(query, (date_A, date_B, tag, name))
        column_names = [column[0] for column in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=column_names)
    finally:
        conn.close()
    return df



async def get_records_by_date(name, db_path, table_name, col1, col2, date_A, date_B):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        query = f"SELECT * FROM {table_name} WHERE {col1} BETWEEN ? AND ? AND name = ?"
        cursor.execute(query, (date_A, date_B, name))
        column_names = [column[0] for column in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=column_names)
    finally:
        conn.close()
    return df