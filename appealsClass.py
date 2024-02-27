import psycopg2
import db_connect
from db_connect import execute_get_sql_query, execute_set_sql_query
from userClass import get_user


def get_appeal_text(appeal_id):
    sql_query = 'SELECT appeal_text FROM appeals WHERE id=%s'
    params = (appeal_id,)
    return execute_get_sql_query(sql_query, params)[0][0]


def set_appeal_text(appeal_id, appeal_text):
    sql_query = 'UPDATE appeals SET appeal_text = %s WHERE id=%s'
    params = (appeal_text, appeal_id,)
    execute_set_sql_query(sql_query, params)


def set_evaluation(appeal_id, evaluation):
    sql_query = 'UPDATE appeals SET evaluation=%s WHERE id=%s'
    params = (evaluation, str(appeal_id),)
    execute_set_sql_query(sql_query, params)


def get_status(appeal_id):
    sql_query = 'SELECT status FROM appeals WHERE id=%s'
    params = (str(appeal_id),)
    return execute_get_sql_query(sql_query, params)


def set_status(appeal_id, status):
    sql_query = 'UPDATE appeals SET status=%s WHERE id=%s'
    params = (str(status), str(appeal_id),)
    execute_set_sql_query(sql_query, params)


def set_date_status(appeal_id, date_status):
    sql_query = 'UPDATE appeals SET date_status=%s WHERE id=%s'
    params = (str(date_status), str(appeal_id),)
    execute_set_sql_query(sql_query, params)


# def add_appeal(user_id, status, category, appeal_text, date, date_status, id_performer, comment, is_appeal_anon,
#                lte_id=None):
#     conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO appeals(user_id, status, category, appeal_text, date, date_status, id_performer, comment, "
#         "is_appeal_anon, lte_id) "
#         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
#         (user_id, status, category, appeal_text, date, date_status, id_performer, comment, is_appeal_anon, lte_id))
#     appeal = cur.fetchone()[0]
#     conn.commit()
#     cur.close()
#     conn.close()
#     return appeal


def add_appeal(user_id, status, category, appeal_text, date, date_status, id_performer, comment, is_appeal_anon,
               lte_id=None, subsubcategory=None):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()

    # Проверьте, существует ли уже обращение с такой же категорией
    cur.execute("SELECT id FROM appeals WHERE category = %s and subsubcategory = %s and appeal_text = %s and "
                "user_id = %s and status = %s and date=%s",
                (category, subsubcategory, appeal_text, str(user_id), status, str(date)))

    existing_appeal = cur.fetchone()

    if existing_appeal:
        # Если обращение с такой же категорией уже существует, верните его id, а не вставляйте новое.
        appeal = existing_appeal[0]
    else:
        # Вставляем новое обращение, если не найдено ни одного существующего обращения с той же категорией
        cur.execute(
            "INSERT INTO appeals(user_id, status, category, appeal_text, date, date_status, id_performer, comment, "
            "is_appeal_anon, lte_id, subsubcategory) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (str(user_id), str(status), str(category), str(appeal_text), str(date), str(date_status), str(id_performer),
             str(comment), is_appeal_anon, lte_id, str(subsubcategory)))

        appeal = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return appeal


def add_appeal_gmail(user_id, category, appeal_text, date):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("INSERT INTO appeals(user_id, category, appeal_text, date) "
                "VALUES ('%s', '%s', '%s', '%s')" % (str(user_id), str(category), str(appeal_text), date))
    conn.commit()
    cur.close()
    conn.close()


def get_appeal_by_id(appeal_id):
    sql_query = "SELECT * FROM appeals WHERE id=%s"
    params = (str(appeal_id),)
    appeals = execute_get_sql_query(sql_query, params)
    return appeals


def get_comment(appeal_id):
    sql_query = 'SELECT comment from appeals WHERE id=%s'
    params = (str(appeal_id),)
    return execute_get_sql_query(sql_query, params)


def set_comment(appeal_id, comment):
    sql_query = 'UPDATE appeals SET comment=%s WHERE id=%s'
    params = (str(comment), str(appeal_id),)
    execute_set_sql_query(sql_query, params)


def set_image_data(appeal_id, file):
    sql_query = 'UPDATE appeals SET image_data=%s WHERE id=%s'
    params = (file.content, appeal_id,)
    execute_set_sql_query(sql_query, params)


def get_image_data(appeal_id):
    sql_query = 'SELECT image_data FROM appeals WHERE id=%s'
    params = (str(appeal_id),)
    row = execute_get_sql_query(sql_query, params)
    import io
    image_data = io.BytesIO(row[0][0])
    return image_data


def get_appeal_text_all(appeal_id):
    appeal_info = get_appeal_by_id(appeal_id)[0]
    user_info = get_user(appeal_info[1])
    # appeal_info = get_appeal_by_id_inner_join_users(appeal_id)[0]
    text = f"Обращения <b>ID</b> {appeal_id}\n\n" \
           f" Статус: {str(appeal_info[2])}\n" \
           f" Дата создания: {str(appeal_info[5])}\n" \
           f" Категория: {str(appeal_info[3])}\n" \
           f" Текст обращения: {str(appeal_info[4])}\n" \
           f" Дата последнего изменения статуса: {str(appeal_info[6])}\n\n" \
           f"Работник\n" \
           f" ФИО: {str(user_info[3])} {str(user_info[2])}\n" \
           f" Табельный номер: {str(user_info[4])}\n" \
           f" Номер телефона: {str(user_info[5])}\n" \
           f" Email: {str(user_info[6])}\n" \
           f" Telegram: {str(user_info[1])}\n" \
           f" Филиал: {str(user_info[7])}\n\n" \
           f" Комментарий: {str(appeal_info[8])}"
    return text


def get_category_by_appeal_id(appeal_id):
    sql_query = "SELECT category from appeals where id=%s"
    params = (appeal_id,)
    return execute_get_sql_query(sql_query, params)
