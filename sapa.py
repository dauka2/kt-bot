import telebot
from telebot import types
import psycopg2

from db_connect import execute_get_sql_query, execute_set_sql_query

def get_photo_by_id(photo_id):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
        cur = conn.cursor()

        # Запрос изображения по ID
        cur.execute("SELECT image_data FROM sapa_link WHERE id = %s", (photo_id,))
        result = cur.fetchone()

        # Закрываем соединение с базой данных
        cur.close()
        conn.close()

        # Если изображение найдено, возвращаем его данные
        if result and result[0]:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении изображения: {e}")
        return None