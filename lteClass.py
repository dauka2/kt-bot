import psycopg2
from db_connect import execute_set_sql_query, execute_get_sql_query


def set_performer_id_i_s(id, performer_id):
    sql_query = "UPDATE internal_sale SET performer_id = %s where id=%s"
    params = (performer_id, id,)
    execute_set_sql_query(sql_query, params)


def set_full_name(id, full_name):
    sql_query = "UPDATE internal_sale SET full_name = %s where id=%s"
    params = (full_name, id,)
    execute_set_sql_query(sql_query, params)


def set_iin(id, iin):
    sql_query = "UPDATE internal_sale SET iin = %s where id=%s"
    params = (iin, id,)
    execute_set_sql_query(sql_query, params)


def set_phone_num_subscriber(id, phone_num):
    sql_query = "UPDATE internal_sale SET phone_num = %s where id=%s"
    params = (phone_num, id,)
    execute_set_sql_query(sql_query, params)


def set_subscriber_type(id, subscriber_type):
    sql_query = "UPDATE internal_sale SET subscriber_type = %s where id=%s"
    params = (subscriber_type, id,)
    execute_set_sql_query(sql_query, params)


def set_is_notified(id, is_notified):
    sql_query = "UPDATE internal_sale SET is_notified = %s where id=%s"
    params = (is_notified, id,)
    execute_set_sql_query(sql_query, params)


def set_subscriber_address(id, subscriber_address):
    sql_query = "UPDATE internal_sale SET subscriber_address = %s where id=%s"
    params = (subscriber_address, id,)
    execute_set_sql_query(sql_query, params)


def set_category_i_s(id, category):
    sql_query = "UPDATE internal_sale SET category = %s where id=%s"
    params = (category, id,)
    execute_set_sql_query(sql_query, params)


def set_product_name(id, product_name):
    sql_query = "UPDATE internal_sale SET product_name = %s where id=%s"
    params = (product_name, id,)
    execute_set_sql_query(sql_query, params)


def set_action(id, action):
    sql_query = "UPDATE internal_sale SET action = %s where id=%s"
    params = (action, id,)
    execute_set_sql_query(sql_query, params)


def set_delivery(id, delivery):
    sql_query = "UPDATE internal_sale SET delivery = %s where id=%s"
    params = (delivery, id,)
    execute_set_sql_query(sql_query, params)


def set_simcard(id, simcard):
    sql_query = "UPDATE internal_sale SET simcard = %s where id=%s"
    params = (simcard, id,)
    execute_set_sql_query(sql_query, params)


def set_modem(id, modem):
    sql_query = "UPDATE internal_sale SET modem = %s where id=%s"
    params = (modem, id,)
    execute_set_sql_query(sql_query, params)


def get_simcard(id):
    sql_query = "SELECT simcard from internal_sale where id = %s"
    params = (id,)
    return execute_get_sql_query(sql_query, params)[0][0]


def add_internal_sale(user_id):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("INSERT INTO internal_sale (user_id) VALUES (%s) RETURNING id", (user_id,))
    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return id


def get_info_internal_sale(id):
    sql_query = "SELECT id, user_id, subscriber_type from internal_sale where id = %s  order by id "
    params = (id,)
    return execute_get_sql_query(sql_query, params)


def delete_internal_sale(id_):
    sql_query = "DELETE from internal_sale where id=%s"
    params = (id_,)
    execute_set_sql_query(sql_query, params)
