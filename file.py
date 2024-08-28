from telebot import *

import performerClass
from appealsClass import get_appeal_by_id, get_image_data, get_appeal_text_all, set_category
from common_file import send_error, get_excel, extract_number, generate_buttons
from db_connect import get_all_appeals_by_id_performer, get_sale, get_appeals
from performerClass import list_categories, get_all_anonymous_appeals_by_id_performer, get_performers_id, \
    get_performers, get_regions, get_categories_by_parentcategory
from userClass import get_user
from user_infoClass import clear_appeals

categories = {
    "Learning.telecom.kz | Техническая поддержка": "1",
    "Обучение | Корпоративный Университет": "2",
    'Портал "Бірлік"': "5",
    "Портал закупок 2.0 | Техническая поддержка": "6",
    "Открытый тендер": "7",
    "Запрос ценовых предложений": "8",
    "Один источник и Электронный магазин": "9",
    "Заключение договоров": "10",
    "Логистика": "11",
    "Транспортировка": "12",
    "EX ЦА": "30",
    "EX ДРБ": "31",
    'EX ДКБ': "32",
    'EX ДИТ': "33",
    'EX КУ': "34",
    'EX СФ': "35",
    'EX ДТК': "36",
    'EX ДУП': "37",
    'EX ОДС Головной ОДС': "38",
    'EX ОДС Центр': "39",
    'EX ОДС Север': "40",
    'EX ОДС Юг': "41",
    'EX ОДС Запад': "42",
    'EX ОДС Восток': "43",
    'EX ОДС Алматы': "44"
}


def admin_appeal(bot, message, message_text):
    if message_text == "Админ панель":
        markup_a = types.ReplyKeyboardMarkup()
        button1_a = types.KeyboardButton("Текущие Обращения")
        button2_a = types.KeyboardButton("Решенные Обращения")
        markup_a.add(button1_a, button2_a)
        bot.send_message(message.chat.id, "Выберите следующий шаг", reply_markup=markup_a)
        return
    elif check_id(str(message.chat.id)) and message_text == "Текущие Обращения":
        appeal_info_ = get_all_appeals_by_id_performer("Обращение принято","В процессе")
        ids = performerClass.get_performer_ids(str(message.chat.id))
        appeal_info = []
        for ap in appeal_info_:
            if str(ap[3]) in ids:
                appeal_info.append(ap)

        markup_a = types.InlineKeyboardMarkup()
        if appeal_info is not None:
            for appeal_ in appeal_info:
                text_b = str(appeal_[0]) + " ID " + appeal_[2] + " " + appeal_[1]
                callback_data_a = str(appeal_[0]) + "admin"
                button_a = types.InlineKeyboardButton(text_b, callback_data=callback_data_a)
                markup_a.add(button_a)
        appeal_info_anon = get_all_anonymous_appeals_by_id_performer(str(message.chat.id), "Обращение принято",
                                                                     "В процессе")
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
    elif check_id(str(message.chat.id)) and message_text == "Решенные Обращения":
        get_excel_admin1(bot, message, "Решено")
    else:
        send_error(bot, message)
        clear_appeals(message)


def get_excel_admin1(bot, message, status="Решено"):
    sql_query = (f"""
    SELECT appeals.id AS "ID",
    users.firstname AS "Имя работника",
    users.lastname AS "Фамилия работника",
    table_number AS "Табельный номер",
    users.phone_number AS "Номер телефона работника",
    users.email AS "Почта",
    branch AS "Филиал",
    status AS "Статус",
    appeals.category AS "Категория",
    appeal_text AS "Текст заявки",
    date AS "Дата создания",
    date_status AS "Дата последнего изменения статуса",
    comment AS "Комментарий",
    evaluation AS "Оценка",
    image_data AS "Фото",
    performers.firstname AS "Имя исполнителя",
    performers.lastname AS "Фамилия исполнителя",
    performers.email AS "Почта исполнителя",
    performers.telegram AS "Телеграм исполнителя"
    FROM appeals 
    INNER JOIN performers ON appeals.id_performer = CAST(performers.id AS VARCHAR) 
    INNER JOIN users ON appeals.user_id = users.id 
    where appeals.status = %s and performers.performer_id = %s""")
    params = (status, str(message.chat.id))
    get_excel(bot, message, get_performers_id(), 'output_file.xlsx', sql_query, params)


def admin_appeal_callback(call, bot, add_comment):
    if extract_number(str(call.data), r'^(\d+)admin$') is not None:
        appeal_id = extract_number(str(call.data), r'^(\d+)admin$')
        appeal_info = get_appeal_by_id(appeal_id)[0]
        image_data = get_image_data(appeal_id)
        try:
            bot.send_photo(appeal_info[7], image_data)
        except:
            print("error")
        callback_d = f"{appeal_id}statusdecided"
        btn_text = "Изменить статус на 'Решено'"
        text = get_appeal_text_all(appeal_id)
        if str(appeal_info[2]) == "Обращение принято":
            callback_d = f"{appeal_id}statusinprocess"
            btn_text = "Изменить статус на 'В процессе'"
            if appeal_info[12] is not None and appeal_info[12] != "":
                lte_info = get_sale(appeal_info[12])
                if lte_info[10] != "Самостоятельно":
                    callback_d = f"{appeal_id}statusdecided"
                    btn_text = "Изменить статус на 'Решено'"
        markup_a = types.InlineKeyboardMarkup(row_width=1)
        button_a = types.InlineKeyboardButton(btn_text, callback_data=callback_d)
        callback_d = f"{appeal_id}addcomment"
        button_a1 = types.InlineKeyboardButton("Добавить комментарий", callback_data=callback_d)
        callback_d = f"{appeal_id}changecategory"
        button_a2 = types.InlineKeyboardButton("Перенаправить в другую категорию", callback_data=callback_d)
        markup_a.add(button_a, button_a1, button_a2)
        bot.send_message(call.message.chat.id, text, reply_markup=markup_a)
    elif extract_number(str(call.data), r'^(\d+)addcomment') is not None:
        appeal_id = extract_number(str(call.data), r'^(\d+)addcomment')
        msg = bot.send_message(call.message.chat.id, 'Введите комментарий')
        bot.register_next_step_handler(msg, add_comment, bot, appeal_id)
    elif extract_number(str(call.data), r'^(\d+)changecategory') is not None:
        appeal_id = extract_number(str(call.data), r'^(\d+)changecategory')
        category_markup = generate_buttons(categories.keys(), types.ReplyKeyboardMarkup(one_time_keyboard=True))
        msg = bot.send_message(call.message.chat.id, 'Выберите категорию', reply_markup=category_markup)
        bot.register_next_step_handler(msg, change_category, bot, appeal_id)


def change_category(message, bot, appeal_id):
    if message.text in categories.keys():
        set_category(appeal_id, message.text)
        appeal_info = get_appeal_by_id(appeal_id)[0]
        text = performer_text(appeal_info)
        performer_id = performerClass.get_performer_id_by_id(appeal_info[7])
        user_id = appeal_info[1]
        bot.send_message(performer_id, "Вам отправлено новое обращение")
        bot.send_message(performer_id, text)
        bot.send_message(user_id, "Ваше обращение было переотправлено в категорию:\n" +
                         message.text)


def performer_text(appeal_info):
    performer_info = performerClass.get_performer_by_id(appeal_info[7])[0]
    text = f"<b>ID</b> {appeal_info[0]}\n\n" \
           f" Статус: {str(appeal_info[2])}\n" \
           f" Дата создания: {str(appeal_info[5])}\n" \
           f" Категория: {str(appeal_info[3])}\n" \
           f" Текст: {str(appeal_info[4])}\n" \
           f" Дата последнего изменения статуса: {str(appeal_info[6])}\n\n" \
           f"Исполнитель\n" \
           f" ФИО: {performer_info[4]} {performer_info[3]}\n" \
           f" Номер телефона: {performer_info[5]}\n" \
           f" Email: {performer_info[6]}\n" \
           f" Telegram: {performer_info[7]}\n\n" \
           f" Комментарий: {str(appeal_info[8])}"
    return text

def check_id(input_id):
    performers = get_performers()
    for performer in performers:
        if str(performer[0]) == str(input_id):
            return True
    return False


def rename_category_to_kaz(kaz_categories, category):
    list_rus_categories = list_categories()
    for i in range(len(kaz_categories)):
        if list_rus_categories[i] == category:
            return kaz_categories[i]
    return category


def rename_category_to_rus(kaz_categories, category):
    for i in range(len(kaz_categories)):
        if kaz_categories[i] == category:
            return list(list_categories())[i]
    return category


def appeal_inline_markup(message, lang="rus", kaz_categories=None):
    markup_a = types.InlineKeyboardMarkup()
    appeals_ = get_appeals(message)
    if appeals_ is None:
        return markup_a
    for appeal in appeals_:
        if lang == "kaz":
            text = str(appeal[0]) + " - " + rename_category_to_kaz(kaz_categories, str(appeal[1]))
        else:
            text = str(appeal[0]) + " - " + appeal[1]
        markup_a.add(types.InlineKeyboardButton(text=text, callback_data=str(appeal[0])))
    return markup_a


def get_user_info(user_id):
    user_info = get_user(user_id)
    text = f"Работник\n" \
           f" ФИО: {str(user_info[2])} {str(user_info[3])}\n" \
           f" Табельный номер: {str(user_info[4])}\n" \
           f" Номер телефона: {str(user_info[5])}\n" \
           f" Email: {str(user_info[6])}\n" \
           f" Telegram: {str(user_info[1])}\n" \
           f" Филиал: {str(user_info[8])}\n"
    return text


def cities_all():
    regions = get_regions()
    cities = []
    for region in regions:
        cities = cities[:] + get_categories_by_parentcategory(region)[:]
    return cities

