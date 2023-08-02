import pandas as pd
import psycopg2
from telebot import *
import kaz
import rus
import db_connect

bot = telebot.TeleBot('6053200189:AAHdUXx0SFKbQBs6S4a06VWw-GgX0KOQpCk')
admin_id = ['484489968', '760906879', '187663574', '577247261', '204504707', '531622371']


@bot.message_handler(commands=['start'])
def start(message):
    # sticker_file = open("images/AnimatedSticker.tgs", "rb")
    # bot.send_sticker(message.chat.id, sticker_file)
    db_connect.creat_db()
    db_connect.addIfNotExistUser(message)
    db_connect.cm_sv_db(message, '/start')
    db_connect.clear_appeals(message)
    if str(message.chat.id)[0] == '-':
        return
    language = db_connect.get_language(message)
    if language[0][0] == 'rus':
        rus.send_welcome_message(bot, message)
    elif language[0][0] == 'kaz':
        kaz.send_welcome_message(bot, message)
    else:
        lang(message)


@bot.message_handler(commands=['language'])
def lang(message):
    if str(message.chat.id)[0] == '-':
        return
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='🇷🇺 Русский язык', callback_data='rus')
    button2 = types.InlineKeyboardButton(text='🇰🇿 Қазақ тілі', callback_data='kaz')
    markup.add(button2, button1)
    bot.send_message(text='Тілді таңдаңыз | Выберите язык', chat_id=message.chat.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'rus')
def handle_button_rus(call):
    db_connect.change_language(call.message, 'rus')
    print(call.message)
    start(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'kaz')
def handle_button_kaz(call):
    db_connect.change_language(call.message, 'kaz')
    start(call.message)


@bot.message_handler(commands=['menu'])
def menu(message):
    db_connect.creat_db()
    db_connect.addIfNotExistUser(message)
    db_connect.cm_sv_db(message, 'menu')
    if str(message.chat.id)[0] == '-':
        return
    language = db_connect.get_language(message)[0][0]
    if language == 'rus':
        rus.menu(bot, message)
    elif language == 'kaz':
        kaz.menu(bot, message)
    else:
        lang(message)
    db_connect.clear_appeals(message)


@bot.message_handler(commands=["help"])
def help(message):
    db_connect.cm_sv_db(message, '/help')
    language = db_connect.get_language(message)[0][0]
    if str(message.chat.id)[0] == '-':
        return
    if language == 'rus':
        bot.send_message(message.chat.id,
                         "Вы можете помочь нам стать лучше и отправить нам письмо на info.ktcu@telecom.kz.")
    elif language == 'kaz':
        bot.send_message(message.chat.id,
                         "Сіз бізге жақсы адам болуға көмектесе аласыз және бізге хат жібере аласыз "
                         "info.ktcu@telecom.kz.")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    language = db_connect.get_language(call.message)[0][0]
    if language == 'rus':
        rus.call_back(bot, call)
    elif language == 'kaz':
        kaz.call_back(bot, call)


@bot.message_handler(commands=['get_excel'])
def get_excel(message):
    # conn = psycopg2.connect(user="postgres", password="j7hPC180")
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")

    df = pd.read_sql_query("SELECT users.id, firstname, lastname, commands_name, commands_history.date  FROM commands_history full outer join users on commands_history.id = users.id", conn)
    df.to_excel('output_file.xlsx', index=False)

    with open('output_file.xlsx', 'rb') as file:
        bot.send_document(message.chat.id, file)
    conn.close()


@bot.message_handler(commands=['get_users_info'])
def get_excel(message):
    # conn = psycopg2.connect(user="postgres", password="j7hPC180")
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    if str(message.chat.id) not in admin_id:
        send_error(message)
    df = pd.read_sql_query("SELECT id, instr, glossar, new_message, chosen_category, appeal_field FROM users_info ", conn)
    df.to_excel('users_info_file.xlsx', index=False)
    with open('users_info_file.xlsx', 'rb') as file:
        bot.send_document(message.chat.id, file)
    conn.close()


@bot.message_handler(commands=['get_users'])
def get_excel(message):
    # conn = psycopg2.connect(user="postgres", password="j7hPC180")
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    if str(message.chat.id) not in admin_id:
        send_error(message)
    df = pd.read_sql_query("SELECT id, firstname, lastname, username FROM users ", conn)
    df.to_excel('users_file.xlsx', index=False)
    with open('users_file.xlsx', 'rb') as file:
        bot.send_document(message.chat.id, file)
    conn.close()


def send_error(message):
    language = db_connect.get_language(message)
    if language == 'rus':
        rus.send_error(bot, message)
    elif language == 'kaz':
        kaz.send_error(bot, message)
    else:
        lang(message)


@bot.message_handler(commands=['broadcast'])
def info_broadcast(message):
    if str(message.chat.id) not in admin_id:
        return
    msg = bot.reply_to(message, 'Введите текст')
    bot.register_next_step_handler(msg, text_check)


def text_check(message):
    markup_text_check = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_yes = types.KeyboardButton("Да")
    button_no = types.KeyboardButton("Нет")
    markup_text_check.add(button_yes, button_no)
    msg = bot.reply_to(message, "Вы уверены что хотите отправить это сообщение?", reply_markup=markup_text_check)
    bot.register_next_step_handler(msg, message_sender, message)


def message_sender(message, broadcast_message):
    if message.text.upper() == "ДА":
        # conn = psycopg2.connect(user="postgres", password="j7hPC180")
        conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
        cur = conn.cursor()
        cur.execute('SELECT id FROM users')
        users_id = cur.fetchall()
        cur.close()
        conn.close()
        for id in users_id:
            if broadcast_message.photo:
                photo_id = broadcast_message.photo[-1].file_id
                bot.send_photo(id[0], photo_id, broadcast_message.caption)

            if broadcast_message.audio:
                audio_id = broadcast_message.audio.file_id
                bot.send_video(id[0], audio_id, broadcast_message.caption)

            if broadcast_message.video:
                video_id = broadcast_message.video.file_id
                bot.send_video(id[0], video_id, broadcast_message.caption)

            if broadcast_message.voice:
                voice_id = broadcast_message.voice.file_id
                bot.send_voice(id[0], voice_id, broadcast_message.caption)

            if broadcast_message.text:
                bot.send_message(id[0], broadcast_message.text)
    elif message.text.upper() == "НЕТ":
        bot.send_message(message.chat.id, "Вызовите функцию /broadcast чтобы вызвать комманду рассылки еще раз")
    else:
        rus.send_error(bot, message)


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message = message.text
    try:
        if str(message.chat.id)[0] == '-':
            return
        language = db_connect.get_language(message)[0][0]
        if language == 'rus':
            text(message, get_message, rus)
        elif language == 'kaz':
            text(message, get_message, kaz)
        else:
            lang(message)
    except:
        lang(message)


def text(message, get_message, lang):
    if get_message in lang.faq_field:
        lang.faq(bot, message)
    elif get_message in lang.faq_1.keys():
        bot.send_message(message.chat.id, lang.faq_1[message.text])
    elif get_message in lang.faq_2.keys():
        bot.send_message(message.chat.id, lang.faq_2[message.text])
    elif get_message in lang.biot_field:
        lang.biot(bot, message)
    elif get_message in lang.kb_field:
        lang.kb(bot, message)
    elif get_message in lang.adapt_field:
        lang.adaption(bot, message)
    elif get_message == "Оставить обращение" or get_message == "Өтінішті қалдыру" \
            or db_connect.get_appeal_field(message):
        lang.appeal(bot, message)
    elif str(message.chat.id) in db_connect.get_users_id():
        if db_connect.get_glossar(message):
            lang.glossary(bot, message)
        elif db_connect.get_instr(message) and message.text in lang.kb_field_all:
            lang.instructions(bot, message)
        else:
            lang.send_error(bot, message)
    else:
        lang.send_error(bot, message)


bot.polling(none_stop=True)
