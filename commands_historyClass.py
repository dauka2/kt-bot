from datetime import datetime, timedelta
from common_file import remove_milliseconds
from db_connect import execute_set_sql_query


def cm_sv_db(message, command_name):
    now = datetime.now() + timedelta(hours=6)
    now_updated = remove_milliseconds(now)
    sql_query = 'INSERT INTO commands_history (id, commands_name, date) VALUES (%s,%s,%s)'
    params = (str(message.chat.id), command_name, now_updated,)
    execute_set_sql_query(sql_query, params)
