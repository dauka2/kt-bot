import psycopg2
from db_connect import execute_get_sql_query, execute_set_sql_query

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

def set_city(user_id, city):
    sql_query = 'UPDATE hse_competitions SET city = %s WHERE user_id = %s'
    params = (city, str(user_id),)
    execute_set_sql_query(sql_query, params)

def set_time(user_id, time):
    sql_query = 'UPDATE hse_competitions SET reg_time = %s WHERE user_id = %s'
    params = (time, str(user_id),)
    execute_set_sql_query(sql_query, params)