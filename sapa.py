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

def update_total_score_by_id(user_id, new_total_score):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
        cur = conn.cursor()

        # Проверяем, существует ли пользователь с указанным user_id
        cur.execute("SELECT email FROM sapa_bonus WHERE id = %s", (str(user_id),))
        result = cur.fetchone()

        if not result:
            return "Пользователь с указанным ID не найден."

        # Получаем email пользователя
        user_email = result[0]

        # Обновляем total_score для email в таблице sapa_bonus
        cur.execute(
            "UPDATE sapa_bonus SET total_score = %s, bonus_score = %s WHERE email = %s",
            (new_total_score, new_total_score, user_email)
        )

        # Подтверждаем изменения
        conn.commit()
        return f"total_score и bonus_score успешно обновлены для пользователя с email: {user_email}."
    except Exception as e:
        return f"Ошибка: {e}"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()