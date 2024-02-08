from telebot import types
import psycopg2

TOKEN = '6145415028:AAEdgPMvSsi3FJw2ccyzWf2QiJrPa_Ycz0A'
admins_id = ['187663574', '760906879']


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


def create_db():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
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
        'image_data bytea, lte_id int)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS performers(id serial primary key, performer_id varchar(50), category varchar(50), '
        'firstname varchar(50), lastname varchar(50), phone_num varchar(13), email varchar(50), telegram varchar(50), '
        'parent_category varchar(50))')
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS internal_sale (
    id SERIAL PRIMARY KEY ,
    user_id VARCHAR(50) NOT NULL,
    performer_id VARCHAR(50),
    full_name VARCHAR(200),
    iin VARCHAR(13),
    phone_num VARCHAR(14),
    subscriber_type VARCHAR(15),
    is_notified BOOLEAN,
    subscriber_address VARCHAR(200),
    product_name VARCHAR(45),
    delivery VARCHAR(30),
    simcard VARCHAR(100),
    modem VARCHAR(100),
    category varchar(50), 
    action varchar(30)
    );
    """
    )
    conn.commit()
    cur.close()
    conn.close()


def addIfNotExistUser(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute('SELECT id FROM users')
    users_id = cur.fetchall()
    if not any(id[0] == str(message.chat.id) for id in users_id):
        cur.execute(
            "INSERT INTO users (id, username, lastname, firstname,table_number, phone_number, email,branch, language) "
            "VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                str(message.chat.id), str(message.from_user.username),
                str(message.from_user.first_name),
                str(message.from_user.last_name), ' ', ' ', ' ', ' ', 'n'))
    cur.execute('SELECT id FROM users_info')
    users_info_id = cur.fetchall()
    if not any(id[0] == str(message.chat.id) for id in users_info_id):
        cur.execute("INSERT INTO users_info(id , instr , glossar, appeal_field, appeal_id, category, is_appeal_anon ) "
                    "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                        str(message.chat.id), False, False, False, 0, ' ', False))
    conn.commit()
    cur.close()
    conn.close()


def delete_performers():
    sql_query = "DROP TABLE IF EXISTS performers"
    execute_set_sql_query(sql_query)


def insert_into_performers():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS performers(id serial primary key, performer_id varchar(50), category varchar(50),'
        'firstname varchar(50), lastname varchar(50), phone_num varchar(13), email varchar(50), telegram varchar(50),'
        'parent_category varchar(50))')

    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) '
                'values (%s, %s, %s, %s, %s, %s, %s)', ("760906879", "Learning.telecom.kz | Техническая поддержка",
                                                        "Мустафина", "Дильназ", "+77009145025", "must.dilnaz@gmail.com",
                                                        "@"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) '
                'values (%s, %s, %s, %s, %s, %s, %s)', ("187663574", "Обучение | Корпоративный Университет",
                                                        "Тамирлан", "Оспанов", "87079089665", "must.dilnaz@gmail.com",
                                                        "@tamirlanospanov"))
    cur.execute("insert into performers (category, email) "
                "values  (%s, %s)", ('Служба поддержки \"Нысана\"', 'must.dilnaz@gmail.com'))
    cur.execute('insert into performers (category, email) '
                'values (%s, %s)', ("Обратиться в службу комплаенс", "must.dilnaz@gmail.com"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) '
                'values (%s, %s, %s, %s, %s, %s, %s)', ("760906879", 'Портал "Бірлік"',
                                                        "Мустафина", "Дильназ", "+77009145025", "must.dilnaz@gmail.com",
                                                        "@"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) values (%s, %s, %s, %s, %s, %s, %s, %s)', ("760906879",
                                                                             "Портал закупок 2.0 | "
                                                                             "Техническая поддержка",
                                                                             "Тотиева", "Жансая", "+77001117777",
                                                                             "@gmail.com",
                                                                             "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) values (%s, %s, %s, %s, %s, %s, %s, %s)', ("760906879",
                                                                             "Открытый тендер",
                                                                             "Копешбаев", "Чингиз", "+77001117777",
                                                                             "@gmail.com",
                                                                             "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) values (%s, %s, %s, %s, %s, %s, %s, %s)', ("760906879",
                                                                             "Запрос ценовых предложений",
                                                                             "Аметова", "Асем", "+77001117777",
                                                                             "@gmail.com",
                                                                             "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) values (%s, %s, %s, %s, %s, %s, %s, %s)', ("760906879",
                                                                             "Один источник и Электронный магазин",
                                                                             "Нурбатшанова", "Нурай", "+77001117777",
                                                                             "@gmail.com",
                                                                             "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) values (%s, %s, %s, %s, %s, %s, %s, %s)', ("760906879",
                                                                             "Заключение договоров",
                                                                             "Уркумбаев", "Руслан", "+77001117777",
                                                                             "@gmail.com",
                                                                             "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) values (%s, %s, %s, %s, %s, %s, %s, %s)', ("760906879",
                                                                             "Логистика",
                                                                             "Азанбеков", "Улан", "+77001117777",
                                                                             "@gmail.com",
                                                                             "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) values (%s, %s, %s, %s, %s, %s, %s, %s)', ("760906879",
                                                                             "Транспортировка",
                                                                             "Азанбеков", "Улан", "+77001117777",
                                                                             "mail.com",
                                                                             "@", "Закупочная деятельность"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Восточно-Казахстанская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Павлодарская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Семипалатинск",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))

    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Актюбинская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Атырауская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Западно-Казахстанская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))

    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("187663574", "Мангистауская ОДТ",
         "Тамирлан", "Оспанов", "87079089665", "@gmail.com", "@tamirlanospanov"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("187663574", "Алматинская ОДТ",
         "Тамирлан", "Оспанов", "87079089665", "@gmail.com", "@tamirlanospanov"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("187663574", "ГЦТ Алматытелеком",
         "Тамирлан", "Оспанов", "87079089665", "@gmail.com", "@tamirlanospanov"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Костанайская ОДТ",
         "Тамирлан", "Оспанов", "87079089665", "@gmail.com", "@tamirlanospanov"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("187663574", "Северо-Казахстанская ОДТ",
         "Тамирлан", "Оспанов", "87079089665", "@gmail.com", "@tamirlanospanov"))

    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Акмолинская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "ГЦТ Астанателеком",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Карагандинская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Жамбылская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Кызылординская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("760906879", "Южно-Казахстанская ОДТ",
         "Дильназ", "Мустафина", "87089081808", "must.dilnaz@gmail.com",
         "@dilnazmustafina"))
    conn.commit()
    cur.close()
    conn.close()


def insert_into_performers_right():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS performers(id serial primary key, performer_id varchar(50), category varchar(50),'
        'firstname varchar(50), lastname varchar(50), phone_num varchar(13), email varchar(100), telegram varchar(50),'
        'parent_category varchar(50))')

    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) '
                'values (%s, %s, %s, %s, %s, %s, %s)', ("1483219013", "Learning.telecom.kz | Техническая поддержка",
                                                        "Людмила", "Нам", "+77009145025", "info.ktcu@telecom.kz", "@"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) '
                'values (%s, %s, %s, %s, %s, %s, %s)', ("187663574", "Обучение | Корпоративный Университет",
                                                        "Тамирлан", "Оспанов", "87079089665", "info.ktcu@telecom.kz",
                                                        "@tamirlanospanov"))
    cur.execute("insert into performers (category, email) "
                "values  (%s, %s)", ('Служба поддержки \"Нысана\"', 'nysana@cscc.kz'))
    cur.execute('insert into performers (category, email) '
                'values (%s, %s)', ("Обратиться в службу комплаенс", "tlek.issakov@telecom.kz"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) '
                'values (%s, %s, %s, %s, %s, %s, %s)', ("760906879", 'Портал "Бірлік"',
                                                        "Айгуль", "Уразбаева", "87064301630", "urazbayeva.a@telecom.kz",
                                                        "@eighth_muse"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) '
                'values (%s, %s, %s, %s, %s, %s, %s, %s)', ("6391020304", "Портал закупок 2.0 | Техническая поддержка",
                                                            "Тотиева", "Жансая", "87001183042", "@gmail.com",
                                                            "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) '
                'values (%s, %s, %s, %s, %s, %s, %s, %s)', ("912472406",
                                                            "Открытый тендер",
                                                            "Копешбаев", "Чингиз", "87753372818",
                                                            "@gmail.com",
                                                            "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) '
                'values (%s, %s, %s, %s, %s, %s, %s, %s)', ("6668716258",
                                                            "Запрос ценовых предложений",
                                                            "Аметова", "Асем", "87001017416",
                                                            "@gmail.com",
                                                            "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) '
                'values (%s, %s, %s, %s, %s, %s, %s, %s)', ("771708608",
                                                            "Один источник и Электронный магазин",
                                                            "Нурбатшанова", "Нурай", "87082904069",
                                                            "@gmail.com",
                                                            "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) '
                'values (%s, %s, %s, %s, %s, %s, %s, %s)', ("1007762084",
                                                            "Заключение договоров",
                                                            "Уркумбаев", "Руслан", "87759718303",
                                                            "@gmail.com",
                                                            "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) '
                'values (%s, %s, %s, %s, %s, %s, %s, %s)', ("6955085517",
                                                            "Логистика",
                                                            "Азанбеков", "Улан", "87077296181",
                                                            "@gmail.com",
                                                            "@", "Закупочная деятельность"))
    cur.execute('insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram, '
                'parent_category) '
                'values (%s, %s, %s, %s, %s, %s, %s, %s)', ("6955085517", "Транспортировка",
                                                            "Азанбеков", "Улан", "87077296181",
                                                            "@gmail.com",
                                                            "@", "Закупочная деятельность"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("5050239407", "Восточно-Казахстанская ОДТ",
         "Айнур", "Жексимбаева", "+77778575527", "zheksimbayeva.a@telecom.kz", "@"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("404353369", "Павлодарская ОДТ",
         "Екатерина", "Стельмах", "87182650045", "Stelmah.E@telecom.kz", "@"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("5469612023", "Семипалатинск",
         "Сауле", "Кажиева", "87232200363", "kazhieva.s@telecom.kz", "@"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Актюбинская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Атырауская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Западно-Казахстанская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Мангистауская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Алматинская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "ГЦТ Алматытелеком",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Костанайская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Северо-Казахстанская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Акмолинская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "ГЦТ Астанателеком",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Карагандинская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Жамбылская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Кызылординская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    cur.execute(
        'insert into performers (performer_id, category, firstname, lastname, phone_num, email, telegram) values '
        '(%s, %s, %s, %s, %s, %s, %s)',
        ("530582651", "Южно-Казахстанская ОДТ",
         "Айжан", "Мухтарканова", "87714371087", "Aizhanmukhtarkanova@gmail.com", "@mukhtarkanova"))
    conn.commit()
    cur.close()
    conn.close()


def alter_table_users():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("drop table performers")
    conn.commit()
    cur.close()
    conn.close()


def get_appeals(message):
    sql_query = "SELECT * FROM appeals inner join performers on performers.category = appeals.category " \
                "WHERE appeals.user_id=%s and status <> %s and performers.id < 13 order by appeals.id"
    params = (str(message.chat.id), "Решено",)
    return execute_get_sql_query(sql_query, params)


def get_all_appeals_by_id_performer(id_performer, status_1, status_2):
    sql_query = (
        'SELECT appeals.id, status, category, appeal_text, date, date_status, comment, '
        'username, firstname, lastname, table_number, phone_number, email '
        'FROM appeals INNER JOIN users ON appeals.user_id = users.id '
        'WHERE appeals.id_performer=%s AND appeals.is_appeal_anon=False AND (status=%s OR status=%s) order by appeals.id'
    )
    params = (str(id_performer), status_1, status_2,)
    appeals = execute_get_sql_query(sql_query, params)
    if appeals:
        return appeals
    return None


def get_appeal_by_id_inner_join_users(id):
    sql_query = (
        'SELECT appeals.id, status, category, appeal_text, date, date_status, comment, '
        'username, firstname, lastname, table_number, phone_number, email, branch, lte_id '
        'FROM appeals INNER JOIN users ON appeals.user_id = users.id '
        'INNER JOIN performers ON appeals.category = performers.category'
        'WHERE appeals.id=%s'
    )
    params = (str(id),)
    appeals = execute_get_sql_query(sql_query, params)
    return appeals


def my_lte(user_id):
    markup_a = types.InlineKeyboardMarkup()
    my_sales = get_sales_by_user_id(user_id)
    for sale in my_sales:
        text = str(sale[0]) + " - " + str(sale[1])
        markup_a.add(types.InlineKeyboardButton(text=text, callback_data=str(sale[0])))
    return markup_a


def get_last_appeal(user_id):
    sql_query = "SELECT MAX(id) from appeals where user_id = %s"
    params = (str(user_id),)
    return execute_get_sql_query(sql_query, params)


def get_appeal_by_lte_id(lte_id):
    sql_query = "SELECT id, appeal_text from appeals where lte_id = %s"
    params = (str(lte_id),)
    return execute_get_sql_query(sql_query, params)[0]


def get_sale(id_i_s):
    sql_query = "SELECT * from internal_sale where id = %s"
    params = (id_i_s,)
    return execute_get_sql_query(sql_query, params)[0]


def get_sales_by_user_id(user_id):
    sql_query = ('SELECT appeals.id, full_name  FROM appeals inner join internal_sale on '
                 'internal_sale.id = appeals.lte_id WHERE appeals.user_id=%s and status <> %s  order by appeals.id')
    params = (str(user_id), "Решено",)
    return execute_get_sql_query(sql_query, params)
