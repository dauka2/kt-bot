import psycopg2
import random
import threading
import time
from db_connect import execute_get_sql_query, execute_set_sql_query


def change_language(message, language):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("UPDATE users SET language='%s' where id='%s'" % (
        str(language), str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()


def generate_and_save_code(user_id):
    verification_code = random.randint(1000, 9999)
    sql_query = "UPDATE users_info SET verif_code = %s WHERE id = %s"
    params = (str(verification_code), user_id)
    execute_set_sql_query(sql_query, params)
    return verification_code


# Функция для получения сохраненного кода из БД
def get_saved_verification_code(user_id):
    sql_query = "SELECT verif_code FROM users_info WHERE id = %s"
    params = (user_id,)
    code = execute_get_sql_query(sql_query, params)[0][0]
    return code


verification_timers = {}


def get_users_id():
    sql_query = 'SELECT id FROM users'
    users = execute_get_sql_query(sql_query)
    users_array = []
    for user in users:
        users_array.append(str(user[0]))
    return users_array


def set_firstname(message, firstname):
    sql_query = 'UPDATE users SET firstname = %s WHERE id=%s'
    params = (firstname, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def set_lastname(message, lastname):
    sql_query = 'UPDATE users SET lastname = %s WHERE id=%s'
    params = (lastname, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_firstname(message):
    sql_query = 'SELECT firstname FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    name = execute_get_sql_query(sql_query, params)[0][0]
    return name


def get_lastname(message):
    sql_query = 'SELECT lastname FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    name = str(execute_get_sql_query(sql_query, params)[0][0])
    return name


def get_language(message):
    sql_query = 'SELECT language FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    name = str(execute_get_sql_query(sql_query, params)[0][0])
    return name


def set_table_number(message, table_num):
    sql_query = 'UPDATE users SET table_number =%s WHERE id=%s'
    params = (table_num, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_table_number(message):
    sql_query = 'SELECT table_number FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def get_phone_number(message):
    sql_query = 'SELECT phone_number FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def get_email(message):
    sql_query = 'SELECT email FROM users WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]

def get_email_for_verif(user_id):
    sql_query = 'SELECT email FROM users WHERE id=%s'
    params = (str(user_id),)
    return execute_get_sql_query(sql_query, params)[0][0]

def set_phone_number(message, phone_number):
    sql_query = 'UPDATE users SET phone_number = %s WHERE id=%s'
    params = (phone_number, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def set_email(message, email):
    sql_query = 'UPDATE users SET email=%s WHERE id=%s'
    params = (email, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_branch(user_id):
    sql_query = 'SELECT users.branch FROM users WHERE id=%s'
    params = (str(user_id),)  # Make sure to create a tuple
    branch = execute_get_sql_query(sql_query, params)
    return branch[0][0] if branch else None


def set_branch(user_id, branch):
    sql_query = 'UPDATE users SET branch=%s WHERE id=%s'
    params = (str(branch), str(user_id),)
    execute_set_sql_query(sql_query, params)


def delete_user(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id='%s'" % (str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()


def delete_users_info():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("DROP TABLE users_info")
    conn.commit()
    cur.close()
    conn.close()

def alter_users():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE")
    conn.commit()
    cur.close()
    conn.close()


def get_user(user_id):
    sql_query = "SELECT * FROM users where id = %s"
    params = (str(user_id),)
    return execute_get_sql_query(sql_query, params)[0]

