import telebot
from telebot import types
import psycopg2

from db_connect import execute_get_sql_query, execute_set_sql_query

def recalculate_scores():
    """
    Пересчитывает баллы пользователей с декабря и обновляет таблицу sapa_bonus.
    Учитывает только записи с is_checked='True' и распределяет баллы по статусу.
    """
    try:
        conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
        cur = conn.cursor()

        # Получаем сумму баллов пользователей из sapa_links с фильтром
        cur.execute("""
            SELECT email, SUM(
                CASE
                    WHEN status = 'пост' THEN 500
                    WHEN status = 'пост1' THEN 1000
                    WHEN status = 'отзыв' THEN 1000
                    WHEN status = 'ничего' THEN 0
                END
            ) as total_score
            FROM sapa_link
            WHERE date >= '2024-01-01 00:00:00' AND is_checked = TRUE
            GROUP BY email
        """)
        scores = cur.fetchall()

        if not scores:
            return "Нет данных для обновления."

        # Обновляем или вставляем данные в sapa_bonus
        for email, total_score in scores:
            # Проверяем, существует ли запись
            cur.execute("SELECT 1 FROM sapa_bonus WHERE email = %s", (email,))
            if cur.fetchone():
                # Если запись существует, обновляем
                cur.execute("""
                    UPDATE sapa_bonus
                    SET total_score = %s, bonus_score = %s
                    WHERE email = %s
                """, (total_score, total_score, email))
            else:
                # Если записи нет, вставляем
                cur.execute("""
                    INSERT INTO sapa_bonus (email, total_score)
                    VALUES (%s, %s)
                """, (email, total_score))

        # Подтверждаем изменения
        conn.commit()

        return f"Баллы успешно пересчитаны для {len(scores)} пользователей."
    except Exception as e:
        print(f"Ошибка при обновлении баллов: {e}")
        return f"Ошибка при обновлении баллов: {e}"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

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