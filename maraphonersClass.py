import psycopg2
from db_connect import execute_get_sql_query, execute_set_sql_query


def insert_into_maraphoners(message):
    sql_query = 'INSERT INTO maraphoners (user_id) VALUES (%s)'
    params = (str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def set_position(message, position):
    sql_query = 'UPDATE maraphoners SET position = %s WHERE user_id=%s'
    params = (position, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def set_age(message, age):
    sql_query = 'UPDATE maraphoners SET age = %s WHERE user_id=%s'
    params = (age, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def set_region(message, region):
    sql_query = 'UPDATE maraphoners SET region = %s WHERE user_id=%s'
    params = (region, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_position(message):
    sql_query = 'SELECT position FROM maraphoners WHERE user_id=%s'
    params = (str(message.chat.id),)
    position = execute_get_sql_query(sql_query, params)[0][0]
    return position


def get_age(message):
    sql_query = 'SELECT age FROM maraphoners WHERE user_id=%s'
    params = (str(message.chat.id),)
    age = execute_get_sql_query(sql_query, params)[0][0]
    return age


def get_region(message):
    sql_query = 'SELECT region FROM maraphoners WHERE user_id=%s'
    params = (str(message.chat.id),)
    region = execute_get_sql_query(sql_query, params)[0][0]
    return region


def get_id(message):
    sql_query = 'SELECT id FROM maraphoners WHERE user_id=%s'
    params = (str(message.chat.id),)
    region = execute_get_sql_query(sql_query, params)[0][0]
    return region
