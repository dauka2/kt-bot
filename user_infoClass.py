from db_connect import execute_set_sql_query, execute_get_sql_query


def set_bool(message, instr, glossar):
    sql_query = 'UPDATE users_info SET instr = %s, glossar =%s WHERE id = %s'
    params = (instr, glossar, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_glossary(message):
    sql_query = 'SELECT glossar FROM users_info WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def get_instr(message):
    sql_query = 'SELECT instr FROM users_info WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def set_appeal_field(message, appeal_field):
    sql_query = 'UPDATE users_info SET appeal_field = %s WHERE id=%s'
    params = (appeal_field, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_appeal_field(message):
    sql_query = 'SELECT appeal_field FROM users_info WHERE id=%s'
    params = (str(message.chat.id),)
    appeal_field = execute_get_sql_query(sql_query, params)
    return appeal_field[0][0]


def set_category(message, category):
    sql_query = 'UPDATE users_info SET category = %s WHERE id=%s'
    params = (category, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def clear_appeals(message):
    sql_query = 'UPDATE users_info SET appeal_id = %s, category = %s, appeal_field = %s, ' \
                'is_appeal_anon=False, subcategory = %s WHERE id=%s'
    params = (0, ' ', False, '', str(message.chat.id))
    execute_set_sql_query(sql_query, params)


def get_category_users_info(message):
    sql_query = 'SELECT category FROM users_info WHERE id=%s'
    params = (str(message.chat.id),)
    appeal_field = execute_get_sql_query(sql_query, params)
    return appeal_field[0][0]


def set_appeal_id(message, id):
    sql_query = 'UPDATE users_info SET appeal_id =%s WHERE users_id=%s'
    params = (id, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_is_appeal_anon_users_info(user_id):
    sql_query = 'SELECT is_appeal_anon from users_info WHERE id=%s'
    params = (str(user_id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def set_is_appeal_anon_users_info(user_id, is_appeal_anon):
    sql_query = 'UPDATE users_info SET is_appeal_anon=%s WHERE id=%s'
    params = (is_appeal_anon, str(user_id),)
    execute_set_sql_query(sql_query, params)


def get_subsubcategory_users_info(user_id):
    sql_query = 'SELECT subcategory from users_info WHERE id=%s'
    params = (str(user_id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def set_subsubcategory_users_info(user_id, subcategory):
    sql_query = 'UPDATE users_info SET subcategory=%s WHERE id=%s'
    params = (subcategory, str(user_id),)
    execute_set_sql_query(sql_query, params)
