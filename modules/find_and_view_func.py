from matplotlib.patches import Patch
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import sqlite3
import random
import os



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



async def plot_col_2_over_time_and_save(df_, col_1, col_2, filename):
  df  = df_.copy()  
  df[col_2] = df[col_2].apply(lambda x: float(x))

  plt.xlabel('Дата')
  plt.ylabel('Расход л/100км')

  plt.plot(df[col_1], df[col_2], marker='o', markerfacecolor='r', linestyle='-', color = 'b', linewidth = '1.7')
  plt.savefig(filename)
  plt.clf()
  return filename



async def plot_fuel(df_, col_1, col_2, filename):
  df  = df_.copy()  
  df[col_1] = pd.to_datetime(df[col_1])  
  df[col_2] = df[col_2].apply(lambda x: float(x))
  fig, ax = plt.subplots()
  plt.xlabel('Дата')
  plt.ylabel('Расход л/100км')

  ax.plot(df[col_1], df[col_2], marker='o', markerfacecolor='r', linestyle='-', color = 'b', linewidth = '1.7')
  ax.xaxis.set_major_locator(mdates.MonthLocator())
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig(filename)
  plt.clf()
  return filename



async def plot_oil(df_, col_1, col_2, filename, bar_width=0.8):
    df = df_.copy()
    df[col_1] = pd.to_datetime(df[col_1])
    df[col_2] = df[col_2].apply(lambda x: float(x))

    fig, ax = plt.subplots()
    grouped_df = df.groupby(col_1)[col_2].sum().reset_index()
    
    num_bars = len(grouped_df)
    bar_width = 1.0 / (num_bars + 1)
    ax.set_xticks([i + (bar_width * (num_bars - 1) / 2) for i in range(len(grouped_df[col_1]))])
    ax.set_xticklabels([datetime.strftime(d, "%d %b %Y") for d in grouped_df[col_1]], rotation=45, ha='center')
    unique_types = df['type'].unique()
    color_map = {
        'Замена масла': 'blue',
        'Доливка масла': 'red',
    }
    for type_ in unique_types:
        if type_ not in color_map:
            color_map[type_] = f'#{random.randint(0, 255):06x}'

    bars = []
    
    for i in range(num_bars):
      bar_positions = [x + i * bar_width for x in range(len(grouped_df[col_1]))]
      bar = ax.bar(bar_positions, grouped_df[col_2], color=[color_map.get(type_, f'#{random.randint(0, 255):06x}') for type_ in df['type']], width=bar_width)
      bars.append(bar)
      for idx, b in enumerate(bar):
        height = b.get_height()
        label_text = f'{height:.2f}'
        label_x = b.get_x() + b.get_width() / 2
        label_y = height + 0.02
        if(i==0):
          ax.text(label_x, label_y, label_text, ha='center', va='bottom')
        
    ax.set_xlabel('Дата')
    ax.set_ylabel('Объем л.')
    plt.legend(handles=[Patch(color=color_map[type_], label=type_) for type_ in unique_types], loc='upper right', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.tight_layout()
    plt.savefig(filename)
    return filename



async def plot_oil_old(df_, col_1, col_2, filename, bar_width=0.0001):
    df = df_.copy()
    df[col_1] = df[col_1].apply(lambda x: datetime.fromtimestamp(float(x)))
    df[col_2] = df[col_2].apply(lambda x: float(x))
  
    plt.xlabel('Дата')
    plt.ylabel('Объем л.')

    unique_types = df['type'].unique()
    color_map = {
        'Замена масла': 'blue',
        'Доливка масла': 'red',
    }
    for type_ in unique_types:
        if type_ not in color_map:
            color_map[type_] = f'#{random.randint(0, 255):06x}'

    bars = plt.bar(df[col_1], df[col_2], color=[color_map[type_] for type_ in df['type']], width=bar_width)
    for bar in bars:
        height = bar.get_height()
        label_text = f'{height:.2f}'
        label_x = bar.get_x() + bar.get_width() / 2
        label_y = height + 0.02

        plt.text(label_x, label_y, label_text, ha='center', va='bottom')

    plt.ylim(bottom=0)
    patches = [Patch(color=color_map[type_], label=type_) for type_ in unique_types]

    plt.legend(handles=patches, loc='upper right', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    filepath = os.path.join(os.getcwd(), filename)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()
    return filename



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