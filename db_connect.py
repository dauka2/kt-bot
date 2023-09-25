import re
from telebot import types
import openpyxl
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import time
from email.header import Header
import smtplib
from email.mime.text import MIMEText
import io

TOKEN = '6220689869:AAHktyMsUH1kA8XePSq3sGIw-zPviXEGEfg'
admins_id = ['187663574', '760906879']


def remove_milliseconds(dt):
    formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    modified_dt = datetime.strptime(formatted_dt, '%Y-%m-%d %H:%M:%S')
    return modified_dt


def get_excel(bot, message, admin_id, excel_file, sql_query, params=None):
    # conn = psycopg2.connect(user="postgres", password="j7hPC180")
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    if str(message.chat.id) not in admin_id:
        send_error(message)
        return
    df = pd.read_sql_query(sql_query, conn, params=params)
    if df.empty:
        bot.send_message(message.chat.id, "Обращения не найдены")
        conn.close()
        return
    df.to_excel(excel_file, index=False)
    with open(excel_file, 'rb') as file:
        bot.send_document(message.chat.id, file)
    conn.close()


def execute_get_sql_query(sql_query, params=None):
    try:
        conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
        cur = conn.cursor()
        cur.execute(sql_query, params)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except (psycopg2.Error, Exception) as e:
        print("Error:", e)
        return None


def execute_set_sql_query(sql_query, params=None):
    try:
        conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
        cur = conn.cursor()
        cur.execute(sql_query, params)
        conn.commit()
        cur.close()
        conn.close()
    except (psycopg2.Error, Exception) as e:
        print("Error:", e)
        return None


def send_error(bot, message):
    bot.send_photo(message.chat.id, photo=open('images/oops_error.jpg', 'rb'))
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Упс, что-то пошло не так...\nПoжaлyйcтa, попробуйте заново запустить бота нажав кнопку /menu")


def create_db():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    # conn = psycopg2.connect(user="postgres", password="j7hPC180")
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id varchar(50) primary key, username varchar(50), lastname varchar(50), '
        'firstname varchar(50), table_number varchar(11), phone_number varchar(13), '
        'email varchar(50), branch varchar(50), language varchar(10))')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS commands_history (id varchar(50), commands_name varchar(50), date timestamp)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users_info(id varchar(50), instr bool, glossar bool, appeal_field bool, '
        'category varchar(50), appeal_id int, is_appeal_anon bool)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS appeals(id serial primary key, user_id varchar(50), status varchar(30), '
        'category varchar(100), appeal_text varchar(1000), date varchar(30), date_status varchar(30), '
        'id_performer varchar(30), comment varchar(1000), is_appeal_anon bool, evaluation int, '
        'image_data bytea)')
    conn.commit()
    cur.close()
    conn.close()


def addIfNotExistUser(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    # conn = psycopg2.connect(user="postgres", password="j7hPC180")
    cur = conn.cursor()
    cur.execute('SELECT id FROM users')
    users_id = cur.fetchall()
    if not any(id[0] == str(message.chat.id) for id in users_id):
        cur.execute("INSERT INTO users (id, username, lastname, firstname,table_number, phone_number, email,branch, language) "
                    "VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (str(message.chat.id), str(message.from_user.username),
                                                              str(message.from_user.first_name),
                                                              str(message.from_user.last_name), ' ', ' ', ' ', ' ', 'n'))
    cur.execute('SELECT id FROM users_info')
    users_info_id = cur.fetchall()
    if not any(id[0] == str(message.chat.id) for id in users_info_id):
        cur.execute("INSERT INTO users_info(id , instr , glossar, appeal_field, appeal_id, category, is_appeal_anon ) "
                    "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (str(message.chat.id), False, False, False, 0, ' ', False))
    conn.commit()
    cur.close()
    conn.close()



def get_language(message):
    # conn = psycopg2.connect(user="postgres", password="j7hPC180")
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT language FROM users WHERE id='%s'" % (str(message.chat.id)))
    language = cur.fetchone()
    cur.close()
    conn.close()
    return language[0]


def change_language(message, language):
    # conn = psycopg2.connect(user="postgres", password="j7hPC180")
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("UPDATE users SET language='%s' where id='%s'" % (
        str(language), str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()




def alter_table_users():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    # cur.execute("ALTER TABLE users ADD COLUMN table_number varchar(11) DEFAULT ' '")
    # cur.execute("ALTER TABLE users ADD COLUMN phone_number varchar(13) DEFAULT ' '")
    # cur.execute("ALTER TABLE users ADD COLUMN email varchar(50) DEFAULT ' '")
    # cur.execute("TRUNCATE users_info")
    # cur.execute("TRUNCATE users")
    # cur.execute("DROP TABLE IF EXISTS users;")
    # cur.execute("DROP TABLE IF EXISTS users_info;")
    # cur.execute("DROP TABLE IF EXISTS appeals;")
    # cur.execute("DROP TABLE IF EXISTS commands_history;")
    # cur.execute("ALTER TABLE users_info DROP COLUMN new_message")
    # cur.execute("ALTER TABLE users_info DROP COLUMN chosen_category")
    # cur.execute(
    #     'CREATE TABLE IF NOT EXISTS appeals(id serial primary key, user_id varchar(50), status varchar(30), '
    #     'category varchar(100), appeal_text varchar(1000), date varchar(30), date_status varchar(30), '
    #     'id_performer varchar(30), comment varchar(1000), is_appeal_anon bool)')
    # cur.execute("ALTER TABLE users ADD COLUMN branch varchar(50) DEFAULT ' '")
    # cur.execute("ALTER TABLE users ADD COLUMN language varchar(10) DEFAULT 'n'")
    # cur.execute("ALTER TABLE users_info ADD COLUMN category varchar(50) DEFAULT False")
    # cur.execute("ALTER TABLE users_info ADD COLUMN appeal_id int DEFAULT 0")
    # cur.execute("ALTER TABLE users_info ADD COLUMN is_appeal_anon bool DEFAULT False")
    # cur.execute("ALTER TABLE appeals ADD COLUMN evaluation int DEFAULT 0")
    cur.execute("ALTER TABLE appeals ADD COLUMN image_data bytea")

    conn.commit()
    cur.close()
    conn.close()


def cm_sv_db(message, command_name):
    now = datetime.now() + timedelta(hours=6)
    now_updated = remove_milliseconds(now)
    sql_query = 'INSERT INTO commands_history (id, commands_name, date) VALUES (%s,%s,%s)'
    params = (str(message.chat.id), command_name, now_updated,)
    execute_set_sql_query(sql_query, params)


def set_bool(message, instr, glossar):
    sql_query = 'UPDATE users_info SET instr = %s, glossar =%s WHERE id = %s'
    params = (instr, glossar, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_glossar(message):
    sql_query = 'SELECT glossar FROM users_info WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def get_instr(message):
    sql_query = 'SELECT instr FROM users_info WHERE id=%s'
    params = (str(message.chat.id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def get_users_id():
    sql_query = 'SELECT id FROM users'
    users = execute_get_sql_query(sql_query)
    users_array = []
    for user in users:
        users_array.append(str(user[0]))
    return users_array


def set_appeal_field(message, appeal_field):
    sql_query = 'UPDATE users_info SET appeal_field = %s WHERE id=%s'
    params = (appeal_field, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_appeal_field(message):
    sql_query = 'SELECT appeal_field FROM users_info WHERE id=%s'
    params = (str(message.chat.id),)
    appeal_field = execute_get_sql_query(sql_query, params)
    return appeal_field[0][0]


def get_appeal_text(appeal_id):
    sql_query = 'SELECT appeal_text FROM appeals WHERE id=%s'
    params = (appeal_id,)
    return execute_get_sql_query(sql_query, params)[0][0]


def set_appeal_text(appeal_id, appeal_text):
    sql_query = 'UPDATE appeals SET appeal_text = %s WHERE id=%s'
    params = (appeal_text, appeal_id,)
    execute_set_sql_query(sql_query, params)


def set_category(message, category):
    sql_query = 'UPDATE users_info SET category = %s WHERE id=%s'
    params = (category, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def clear_appeals(message):
    sql_query = 'UPDATE users_info SET appeal_id = %s, category = %s, appeal_field = %s, ' \
                'is_appeal_anon=False WHERE id=%s'
    params = (0, ' ', False, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def get_category_users_info(message):
    sql_query = "SELECT category FROM users_info WHERE id = %s;"
    params = (str(message.chat.id),)
    category = execute_get_sql_query(sql_query=sql_query, params=params)
    if category:
        return category[0][0]
    else:
        return None


def set_appeal_id(message, id):
    sql_query = 'UPDATE users_info SET appeal_id =%s WHERE users_id=%s'
    params = (id, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def send_gmails(text, categories, category):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sending1001@gmail.com", "njdhfqafaajixebg")
    msg = MIMEText(text, 'plain', 'utf-8')
    subject = category
    msg['Subject'] = Header(subject, 'utf-8')
    s.sendmail("sending1001@gmail.com", categories[category], msg.as_string())
    s.quit()


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


def set_phone_number(message, phone_number):
    sql_query = 'UPDATE users SET phone_number = %s WHERE id=%s'
    params = (phone_number, str(message.chat.id),)
    execute_set_sql_query(sql_query, params)


def set_email(message, email):
    sql_query = 'UPDATE users SET email=%s WHERE id=%s'
    params = (email, str(message.chat.id),)
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



def add_appeal(user_id, status, category, appeal_text, date, date_status, id_performer, comment, is_appeal_anon):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    # conn = psycopg2.connect(user="postgres", password="j7hPC180")
    cur = conn.cursor()
    cur.execute("INSERT INTO appeals(user_id, status, category, appeal_text, date, date_status, id_performer, comment,"
                "is_appeal_anon) VALUES "
                "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') RETURNING id"
                % (str(user_id), status, category, appeal_text, date, date_status, id_performer, comment, is_appeal_anon))
    appeal = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return appeal



def get_appeals(message):
    sql_query = 'SELECT id, category FROM appeals WHERE user_id=%s and status <> %s'
    params = (str(message.chat.id), "Решено", )
    return execute_get_sql_query(sql_query, params)


def get_appeal_by_id(id):
    sql_query = "SELECT * FROM appeals WHERE id=%s"
    params = (str(id), )
    appeals = execute_get_sql_query(sql_query, params)
    return appeals



def get_all_appeals_by_id_performer(id_performer, status_1, status_2):
    sql_query = (
        'SELECT appeals.id, status, category, appeal_text, date, date_status, comment, '
        'username, firstname, lastname, table_number, phone_number, email '
        'FROM appeals INNER JOIN users ON appeals.user_id = users.id '
        'WHERE appeals.id_performer=%s AND appeals.is_appeal_anon=False AND (status=%s OR status=%s)'
    )
    params = (str(id_performer), status_1, status_2,)
    appeals = execute_get_sql_query(sql_query, params)
    if appeals:
        return appeals
    return None


def get_all_anonymous_appeals_by_id_performer(id_performer, status_1, status_2):
    sql_query = (
        'SELECT * from appeals WHERE is_appeal_anon=TRUE and id_performer=%s and (status=%s or status=%s)'
    )
    params = (str(id_performer), status_1, status_2,)
    appeals = execute_get_sql_query(sql_query, params)
    if appeals:
        return appeals
    return None


def get_appeal_by_id_inner_join_users(id):
    sql_query = (
        'SELECT appeals.id, status, category, appeal_text, date, date_status, comment, '
        'username, firstname, lastname, table_number, phone_number, email, branch '
        'FROM appeals INNER JOIN users ON appeals.user_id = users.id '
        'WHERE appeals.id=%s'
    )
    params = (str(id),)
    appeals = execute_get_sql_query(sql_query, params)
    return appeals


def get_branch(user_id):
    sql_query = 'SELECT users.branch FROM users WHERE id=%s'
    params = (str(user_id),)  # Make sure to create a tuple
    branch = execute_get_sql_query(sql_query, params)
    return branch[0][0] if branch else None


def set_branch(user_id, branch):
    sql_query = 'UPDATE users SET branch=%s WHERE id=%s'
    params = (str(branch), str(user_id),)
    execute_set_sql_query(sql_query, params)


def get_comment(appeal_id):
    sql_query = 'SELECT comment from appeals WHERE id=%s'
    params = (str(appeal_id),)
    return execute_get_sql_query(sql_query, params)


def set_comment(appeal_id, comment):
    sql_query = 'UPDATE appeals SET comment=%s WHERE id=%s'
    params = (str(comment), str(appeal_id),)
    execute_set_sql_query(sql_query, params)


def get_is_appeal_anon_users_info(user_id):
    sql_query = 'SELECT is_appeal_anon from users_info WHERE id=%s'
    params = (str(user_id),)
    return execute_get_sql_query(sql_query, params)[0][0]


def set_is_appeal_anon_users_info(user_id, is_appeal_anon):
    sql_query = 'UPDATE users_info SET is_appeal_anon=%s WHERE id=%s'
    params = (is_appeal_anon, str(user_id),)
    execute_set_sql_query(sql_query, params)


def set_image_data(appeal_id, file):
    sql_query = 'UPDATE appeals SET image_data=%s WHERE id=%s'
    params = (file.content, appeal_id,)
    execute_set_sql_query(sql_query, params)


def get_image_data(appeal_id):
    sql_query = 'SELECT image_data FROM appeals WHERE id=%s'
    params = (str(appeal_id),)
    row = execute_get_sql_query(sql_query, params)
    image_data = io.BytesIO(row[0][0])
    return image_data



def delete_user(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id='%s'" % (str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()



def glossary(bot, message, text1, text2):
    wb = openpyxl.load_workbook('glossary.xlsx')
    excel = wb['Лист1']
    abbr, defs = [], []
    for row in excel.iter_rows(min_row=2, max_row=1264, values_only=True):
        abbr.append(row[1])
        defs.append(row[2])
    if message.text.upper() in abbr:
        index = abbr.index(message.text.upper())
        text1 += f" \n{defs[index]}"
        bot.send_message(message.chat.id, text1)
    else:
        bot.send_photo(message.chat.id, photo=open('images/oops.jpg', 'rb'))
        bot.send_message(message.chat.id, text2)


def generate_buttons(bts_names, markup_g):
    for button_g in bts_names:
        markup_g.add(types.KeyboardButton(button_g))
    return markup_g


def useful_links():
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='Телеграм telecom.kz', url='https://t.me/kazakhtelecom_official')
    button2 = types.InlineKeyboardButton(text='KTCU Фотобанк', url='https://t.me/kazakhtelecomKTCU')
    button3 = types.InlineKeyboardButton(text='KTCU Инстаграм',
                                         url='https://www.instagram.com/kazakhtelecom_university/')
    button4 = types.InlineKeyboardButton(text='EX | Вопросы и обращения', url='https://t.me/contactingKT')
    button5 = types.InlineKeyboardButton(text='СФ чат', url='https://t.me/sf_kazakhtelecom')
    button6 = types.InlineKeyboardButton(text='Промышленный чат-бот', url='https://t.me/Lira_SF_bot')
    button7 = types.InlineKeyboardButton(text='Забота о сотрудниках', url='https://t.me/+I8Okb3LFgKExYWZi')
    markup.add(button1, button2, button3, button4, button5, button6, button7)
    return markup


def extract_number_from_status_change(input_string, pattern):
    match = re.match(pattern, input_string)
    if match:
        return int(match.group(1))
    else:
        return None


def extract_numbers_from_status_change_decided(input_string):
    pattern = r'(\d+)evaluation(\d+)'
    match = re.search(pattern, input_string)
    if match:
        # Возвращает кортеж из двух чисел
        return int(match.group(1)), int(match.group(2))
    else:
        return None


def admin_appeal(bot, message, message_text, categories):
    if message_text == "Админ панель для обращений":
        markup_a = types.ReplyKeyboardMarkup()
        button1_a = types.KeyboardButton("Текущие Обращения")
        button2_a = types.KeyboardButton("Решенные Обращения")
        markup_a.add(button1_a, button2_a)
        bot.send_message(message.chat.id, "Выберите следующий шаг", reply_markup=markup_a)
        return
    elif check_id(categories, str(message.chat.id)) and message_text == "Текущие Обращения":
        appeal_info = get_all_appeals_by_id_performer(str(message.chat.id), "Обращение принято", "В процессе")
        markup_a = types.InlineKeyboardMarkup()
        if appeal_info is not None:
            for appeal_ in appeal_info:
                text_b = str(appeal_[0]) + " ID " + appeal_[9] + " " + appeal_[8]
                callback_data_a = str(appeal_[0]) + "admin"
                button_a = types.InlineKeyboardButton(text_b, callback_data=callback_data_a)
                markup_a.add(button_a)
        appeal_info_anon = get_all_anonymous_appeals_by_id_performer(str(message.chat.id), "Обращение принято", "В процессе")
        if appeal_info_anon is not None:
            for appeal_ in appeal_info_anon:
                text_b = str(appeal_[0]) + " Анонимно"
                callback_data_a = str(appeal_[0]) + "admin"
                button_a = types.InlineKeyboardButton(text_b, callback_data=callback_data_a)
                markup_a.add(button_a)
        elif markup_a.keyboard:
            bot.send_message(message.chat.id, "Текущие Обращения", reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, "Текущих Обращений нет")
    elif check_id(categories, str(message.chat.id)) and message_text == "Решенные Обращения":
        get_excel_admin1(bot, message, "Решено")
    else:
        send_error(bot, message)
        clear_appeals(message)


def get_excel_admin1(bot, message, status="Решено"):
    sql_query = "SELECT * from appeals where id_performer=%s and status=%s"
    params = (str(message.chat.id), str(status),)  # Make sure to create a tuple
    get_excel(bot, message, admins_id, 'output_file.xlsx', sql_query, params)


def appealInlineMarkup(message):
    markup_a = types.InlineKeyboardMarkup()
    appeals_ = get_appeals(message)
    for appeal in appeals_:
        text = str(appeal[0]) + " - " + appeal[1]
        markup_a.add(types.InlineKeyboardButton(text=text, callback_data=str(appeal[0])))
    return markup_a


def admin_appeal_callback(call, bot, add_comment):
    if extract_number_from_status_change(str(call.data), r'^(\d+)admin$') is not None:
        appeal_id = extract_number_from_status_change(str(call.data), r'^(\d+)admin$')
        appeal_info = get_appeal_by_id(appeal_id)[0]
        image_data = get_image_data(appeal_id)
        try:
            bot.send_photo(appeal_info[1], image_data)
        except:
            print("error")
        callback_d = f"{appeal_id}statusdecided"
        btn_text = "Изменить статус на Решено"
        if appeal_info[9]:
            text = f"ID обращения {appeal_id}\n\n" \
                   f" Статус: {str(appeal_info[2])}\n" \
                   f" Дата создания: {str(appeal_info[5])}\n" \
                   f" Категория: {str(appeal_info[3])}\n" \
                   f" Текст обращения: {str(appeal_info[4])}\n" \
                   f" Дата последнего изменения статуса: {str(appeal_info[6])}" \
                   f" Комментарий: {str(appeal_info[8])}\n\n"
            if str(appeal_info[2]) == "Обращение принято":
                callback_d = f"{appeal_id}statusinprocess"
                btn_text = "Изменить статус на 'В процессе'"
        else:
            appeal_info = get_appeal_by_id_inner_join_users(appeal_id)[0]
            text = f"ID обращения {appeal_id}\n\n" \
                   f" Статус: {str(appeal_info[1])}\n" \
                   f" Дата создания: {str(appeal_info[4])}\n" \
                   f" Категория: {str(appeal_info[2])}\n" \
                   f" Текст обращения: {str(appeal_info[3])}\n" \
                   f" Дата последнего изменения статуса: {str(appeal_info[5])}" \
                   f" Комментарий: {str(appeal_info[6])}\n\n" \
                   f"Пользователь\n" \
                   f" ФИО: {str(appeal_info[9])} {str(appeal_info[8])}\n" \
                   f" Номер телефона: {str(appeal_info[11])}\n" \
                   f" Email: {str(appeal_info[12])}\n" \
                   f" Telegram: {str(appeal_info[7])}\n" \
                   f" Филиал: {str(appeal_info[13])}"
            if str(appeal_info[1]) == "Обращение принято":
                callback_d = f"{appeal_id}statusinprocess"
                btn_text = "Изменить статус на 'В процессе'"
        markup_a = types.InlineKeyboardMarkup(row_width=1)
        button_a = types.InlineKeyboardButton(btn_text, callback_data=callback_d)
        callback_d = f"{appeal_id}addcomment"
        button_a1 = types.InlineKeyboardButton("Добавить комментарий", callback_data=callback_d)
        markup_a.add(button_a, button_a1)
        bot.send_message(call.message.chat.id, text, reply_markup=markup_a)
    # elif extract_number_from_status_change(str(call.data), r'^(\d+)statusinprocess') is not None \
    #      or extract_number_from_status_change(str(call.data), r'^(\d+)statusdecided$') is not None:
    #     appeal_id = extract_number_from_status_change(str(call.data), r'^(\d+)statusinprocess')
    #     if appeal_id is None:
    #         appeal_id = extract_number_from_status_change(str(call.data), r'^(\d+)statusdecided$')
    #         set_status(appeal_id, "Решено")
    #     else:
    #         set_status(appeal_id, "В процессе")
    #     now = datetime.now() + timedelta(hours=6)
    #     now_updated = remove_milliseconds(now)
    #     set_date_status(appeal_id, str(now_updated))
    #     bot.send_message(call.message.chat.id, "Статус изменен")
    elif extract_number_from_status_change(str(call.data), r'^(\d+)addcomment') is not None:
        appeal_id = extract_number_from_status_change(str(call.data), r'^(\d+)addcomment')
        msg = bot.send_message(call.message.chat.id, 'Введите комментарий')
        bot.register_next_step_handler(msg, add_comment, bot, appeal_id)



def check_id(categories, input_id):
    for category, details in categories.items():
        if details.get("id") == input_id:
            return True
    return False
