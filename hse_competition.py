import psycopg2
from db_connect import execute_get_sql_query, execute_set_sql_query


def check_user_exists(user_id):
    """
    Проверяет, существует ли запись с данным user_id в базе данных.

    :param user_id: ID пользователя, который нужно проверить.
    :return: True, если пользователь существует, иначе False.
    """
    sql_query = 'SELECT EXISTS (SELECT 1 FROM hse_competitions WHERE user_id = %s)'
    params = (str(user_id),)
    result = execute_get_sql_query(sql_query, params)
    return result[0]  # возвращает True или False в зависимости от результата запроса

def insert_into_hse_competition(user_id):
    sql_query = 'INSERT INTO hse_competitions (user_id) VALUES (%s)'
    params = (str(user_id),)
    execute_set_sql_query(sql_query, params)


def set_competition(user_id, competition_name):
    sql_query = 'UPDATE hse_competitions SET competition_name = %s WHERE user_id = %s'
    params = (competition_name, str(user_id),)
    execute_set_sql_query(sql_query, params)


def set_position(user_id, position):
    sql_query = 'UPDATE hse_competitions SET position = %s WHERE user_id = %s'
    params = (position, str(user_id),)
    execute_set_sql_query(sql_query, params)


def set_city(user_id, position):
    sql_query = 'UPDATE hse_competitions SET city = %s WHERE user_id = %s'
    params = (position, str(user_id),)
    execute_set_sql_query(sql_query, params)

