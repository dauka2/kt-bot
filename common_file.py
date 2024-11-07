import re
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import telebot
from telebot import types
import openpyxl
import pandas as pd
import psycopg2
from datetime import datetime
import time
from email.header import Header
import smtplib
from email.mime.text import MIMEText
import requests
from difflib import get_close_matches


from performerClass import get_email_by_category
from userClass import get_email_for_verif


def remove_milliseconds(dt):
    formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    modified_dt = datetime.strptime(formatted_dt, '%Y-%m-%d %H:%M:%S')
    return modified_dt


def send_error(bot, message):
    send_photo_(bot, message.chat.id, 'images/oops_error.jpg')
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Упс, что-то пошло не так...\nПoжaлyйcтa, попробуйте заново запустить бота нажав кнопку /menu")


def get_excel(bot, message, admin_id, excel_file, sql_query, params=None):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    if str(message.chat.id) not in admin_id:
        send_error(bot, message)
        return
    df = pd.read_sql_query(sql_query, conn, params=params)
    if df.empty:
        bot.send_message(message.chat.id, "Информация не найдена")
        conn.close()
        return
    df.to_excel(excel_file, index=False)
    with open(excel_file, 'rb') as file:
        bot.send_document(message.chat.id, file)
    conn.close()


def send_gmails(text, category, file_url=None):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sending1001@gmail.com", "njdhfqafaajixebg")
    msg = MIMEMultipart()
    msg['From'] = "sending1001@gmail.com"
    msg['Subject'] = Header(category, 'utf-8')
    msg.attach(MIMEText(text, 'plain', 'utf-8'))
    if file_url is not None:
        response = requests.get(file_url)
        if response.status_code == 200:
            photo_data = response.content
            photo = MIMEImage(photo_data, name='photo.jpg')
            msg.attach(photo)
    email = get_email_by_category(category)
    s.sendmail("sending1001@gmail.com", email, msg.as_string())
    s.quit()


def send_gmails_for_verif(text, user_id, file_url=None):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sending1001@gmail.com", "njdhfqafaajixebg")
    msg = MIMEMultipart()
    msg['From'] = "sending1001@gmail.com"
    msg['Subject'] = Header("Верификация аккаунта", 'utf-8')
    msg.attach(MIMEText(text, 'plain', 'utf-8'))
    if file_url is not None:
        response = requests.get(file_url)
        if response.status_code == 200:
            photo_data = response.content
            photo = MIMEImage(photo_data, name='photo.jpg')
            msg.attach(photo)
    email = get_email_for_verif(str(user_id))
    s.sendmail("sending1001@gmail.com", email, msg.as_string())
    s.quit()


def glossary(bot, message, text1, text2, button_text):
    wb = openpyxl.load_workbook('glossary.xlsx')
    excel = wb['Лист1']
    abbr, defs = [], []
    for row in excel.iter_rows(min_row=2, max_row=1500, values_only=True):
        abbr.append(str(row[1]).upper())
        defs.append(row[2])
    if message.text.upper() in abbr:
        indexes = [index for index, value in enumerate(abbr) if value == message.text.upper()]
        for i in indexes:
            text1 += "\n" + defs[i]
        bot.send_message(message.chat.id, text1)
    else:
        close_matches = get_close_matches(message.text.upper(), abbr, n=5, cutoff=0.6)
        matches_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        matches_markup = generate_buttons(close_matches, matches_markup)
        send_photo_(bot, message.chat.id, 'images/oops.jpg')
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(button_text, callback_data="abbr")
        markup.add(button)
        bot.send_message(message.chat.id, text2, reply_markup=markup)
        if close_matches:
            bot.send_message(message.chat.id, "Вы также можете выбрать похожее значение из списка",
                             reply_markup=matches_markup)


def generate_buttons(bts_names, markup_g):
    for button_g in bts_names:
        markup_g.add(types.KeyboardButton(str(button_g)))
    return markup_g


def useful_links():
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='Телеграм telecom.kz', url='https://t.me/kazakhtelecom_official')
    button2 = types.InlineKeyboardButton(text='KTCU Фотобанк', url='https://t.me/kazakhtelecomKTCU')
    button3 = types.InlineKeyboardButton(text='KTCU Инстаграм',
                                         url='https://www.instagram.com/kazakhtelecom_university/')
    button5 = types.InlineKeyboardButton(text='СФ чат', url='https://t.me/sf_kazakhtelecom')
    button6 = types.InlineKeyboardButton(text='Промышленный чат-бот', url='https://t.me/Lira_SF_bot')
    # button7 = types.InlineKeyboardButton(text='Чат-бот ОДС', url='https://t.me/Lira_SF_bot')
    markup.add(button1, button2, button3, button5, button6)
    return markup


def extract_number(input_string, pattern):
    match = re.match(pattern, input_string)
    if match:
        try:
            return int(match.group(1))
        except Exception as ex:
            print(ex.args)
            return None
    return None


def extract_text(input_string, pattern, t):
    match = re.search(pattern, input_string)
    if match:
        return input_string.replace(t, "")
    else:
        return None


def extract_numbers_from_status_change_decided(input_string):
    pattern = r'(\d+)evaluation(\d+)'
    match = re.search(pattern, input_string)
    if match:
        return int(match.group(1)), int(match.group(2))
    else:
        return None


def check_portal_guide(bot, message, message_text, portal_guide):
    if message_text == portal_guide[0]:
        bot.send_message(str(message.chat.id), "ФФФАААЙЙЙЛЛЛ1")
    elif message_text == portal_guide[1]:
        bot.send_message(str(message.chat.id), "ФФФАААЙЙЙЛЛЛ2")
    elif message_text == portal_guide[2]:
        bot.send_message(str(message.chat.id), "ФФФАААЙЙЙЛЛЛ3")
    elif message_text == portal_guide[3]:
        bot.send_message(str(message.chat.id), "ФФФАААЙЙЙЛЛЛ4")
    elif message_text == portal_guide[4]:
        bot.send_message(str(message.chat.id), "ФФФАААЙЙЙЛЛЛ5")
    elif message_text == portal_guide[5]:
        bot.send_message(str(message.chat.id), "ФФФАААЙЙЙЛЛЛ6")
    elif message_text == portal_guide[6]:
        bot.send_message(str(message.chat.id), "ФФФАААЙЙЙЛЛЛ7")
    elif message_text == portal_guide[7]:
        bot.send_message(str(message.chat.id), "ФФФАААЙЙЙЛЛЛ8")
    elif message_text == portal_guide[8]:
        bot.send_message(str(message.chat.id), "ФФФАААЙЙЙЛЛЛ9")
    else:
        send_error(bot, message)


def send_photo_(bot, message_id, file_path):
    try:
        photo = open(file_path, 'rb')
        bot.send_photo(message_id, photo)
        photo.close()
    except telebot.apihelper.ApiTelegramException as e:
        print(f"An error occurred while sending a photo: {e}")