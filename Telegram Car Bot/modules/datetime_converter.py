import datetime 

def convert_date_to_datetime(date_string):
  try:
    day, month, year = date_string.split('-')

    day = int(day)
    month = int(month)
    year = int(year)

    date_object = datetime.date(year, month, day)

    return date_object
  except ValueError:
    print("Неверный формат даты. Пожалуйста, используйте формат 'день-месяц-год'.")
    return None