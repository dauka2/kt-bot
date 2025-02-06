import types
from datetime import timedelta
import pandas as pd
import requests
from telebot import *
import io
import re
from telebot.apihelper import download_file

import appealsClass
import common_file
import db_connect
import lteClass
import performerClass
import maraphonersClass
from appealsClass import set_status, set_date_status, get_appeal_by_id, get_image_data, get_status, set_evaluation, \
    get_appeal_text_all, get_comment, set_comment, set_image_data, add_appeal_gmail, add_appeal, get_appeal_text, \
    set_appeal_text, set_appeal_id
from commands_historyClass import cm_sv_db
from common_file import (extract_text, extract_number, remove_milliseconds,
                         extract_numbers_from_status_change_decided, generate_buttons, send_gmails, useful_links,
                         check_portal_guide,
                         send_photo_)
from file import check_id, admin_appeal_callback, appeal_inline_markup, admin_appeal, get_user_info
from lteClass import add_internal_sale, set_subscriber_type, set_category_i_s, set_performer_id_i_s, set_is_notified, \
    set_full_name, set_iin, set_phone_num_subscriber, set_subscriber_address, set_product_name, set_action, \
    set_delivery, set_simcard, set_modem, delete_internal_sale
from performerClass import get_performer_by_category, get_regions, list_categories, get_categories_by_parentcategory, \
    get_performer_id_by_category, get_subsubcategories_by_subcategory, \
    get_performer_by_category_and_subcategory, get_performer_by_subsubcategory, get_performers_
from sapa import get_photo_by_id
from userClass import get_branch, get_firstname, get_user, generate_and_save_code, get_email, \
    set_email, verification_timers, get_saved_verification_code, get_lastname, get_phone_number, \
    get_user_verification_status, check_if_registered, delete_participation, check_registration_message_in_history, \
    check_registration_message_in_history_decl, \
    get_user_verification_status_reg, \
    delete_registration_message_in_history, get_verif_decl_status
from user_infoClass import set_appeal_field, get_category_users_info, set_category, get_appeal_field, clear_appeals, \
    set_bool, set_subsubcategory_users_info, get_subsubcategory_users_info
import hse_competition

faq_field = ["Часто задаваемые вопросы", "Демеу", "Вопросы к HR", "Вопросы по займам",
             "Вопросы по закупочной деятельности", "Вопросы по порталу закупок"]
drb_regions = ["Алматинский регион, г.Алматы", "Западный, Центральный регион", "Северный, Южный, Восточный регионы"]
ods_regions = ["ДЭСД 'Алматытелеком'", "Южно-Казахстанский ДЭСД", "Кызылординский ДЭСД", "Костанайский ДЭСД",
               "Восточно-Казахстанский ДЭСД", "Атырауский ДЭСД", "Актюбинский ДЭСД",
               "ДЭСД 'Астана'", "ТУСМ-1", "ТУСМ-6", "ТУСМ-8", "ТУСМ-10", "ТУСМ-11", "ТУСМ-13", "ТУСМ-14", "ГА"]
biot_field = ["👷Заполнить карточку БиОТ", "Опасный фактор/условие", "Поведение при выполнении работ",
              "Предложения/Идеи"]
kb_field = ["🗃️База знаний", "База инструкций", "Глоссарий", "Полезные ссылки", "Сервис и Продажи",
            "Регламентирующие документы"]
kb_field_all = ["Логотипы и Брендбук", "Личный кабинет telecom.kz", "Модемы | Настройка", "Lotus | Инструкции",
                "CheckPoint VPN | Удаленная работа", "Командировка | Порядок оформления",
                "Как авторизоваться", "Личный профиль", "Из портала перейти в ССП",
                "Данные по серверам филиалов", "Инструкция по установке Lotus", "Установочный файл Lotus",
                "АО 'Казахтелеком'", 'Как посмотреть подключенные услуги', 'Как оплатить услугу',
                'Как посмотреть о деталях оплаты', "Раздел 'Мои Услуги'",
                "Корпоративный университет", "ADSL модем", "IDTV приставки",
                "ONT модемы", "Router 4G and Router Ethernet", "Инструкция по установке CheckPoint",
                "Установочный файл CheckPoint", "Портал закупок | Инструкции", 'Для инициаторов | Инструкции',
                'Для секретарей | Инструкции', 'Улучшение Wi-Fi сигнала для абонентов',
                'Настройка маршрутизатора и Mesh системы', 'Сеть и ТВ+', 'Сетевая настройка и TCP/IP',
                'Установка ТВ+ Казахтелеком', 'Подключение телевизора в Wi-fi', 'Измерительные приборы',
                'Измерительные приборы инструкция', 'Аннотация Инструкция для работы с измерительным прибором',
                'Инструкция для прохождения курсов ДО']
instr_field = ["Брендбук и логотипы", "Личный кабинет telecom.kz", "Модемы | Настройка", "Lotus & CheckPoint"]
adapt_field = ["😊Welcome курс | Адаптация", "ДТК", "Общая информация", "Орг структура", "Приветствие", "История",
               "ДТК Инструкции", "Заявки в ОЦО HR", "Заявки возложение обязанностей", "Заявки на отпуск",
               "Командировки", "Переводы", "Порядок оформления командировки", "Рассторжение ТД"]
maraphon_field = ["🚀Цифровой марафон | Регистрация"]
fin_gram_field = ['💸Регистрация на обучение "Финансовая грамотность"']
modems_field = ['📶SAPA+']
hse_competition_field = ["👷🏻‍♂️Конкурсы по охране труда"]
hse_com_field = ["Мой безопасный рабочий день/Менің қауіпсіз жұмыс күнім", "Лучший совет по безопасности/Ең жақсы қауіпсіздік кеңесі", "Принять участие в обоих конкурсах/Екі байқауға қатысу"]
verification_field = ["📄Подтверждение сдачи декларации"]
portal_bts = ["Что такое портал 'Бірлік'?", "Как войти на портал?"
    # , "Оставить обращение на портал"
              ]
sapa_admin = ['1066191569', '353845928', '947621727', '468270698', '531622371', '1621516433', '477945972', '577247261', '735766161', '476878708', '597334185', '559872057', '510122980']
# "Бірлік Гид"
portal_ = ["Мобильная версия", "ПК или ноутбук", "Как авторизоваться", "Личный профиль", "Из портала перейти в ССП",
           "iOS", "Android", "Есть checkpoint", "Нет checkpoint"]
portal_guide = ["Куда обратиться для обратной связи - комментарии и предложения?",
                "Где на портале можно ознакомиться со стратегией компании?",
                "Как создать сообщество?", "Как запланировать отпуск в экосистеме?",
                "Как поблагодарить коллегу?", "Как создать опрос в экосистеме?",
                "Как купить товар со скидкой в Казахтелеком магазине?", "Как купить мерч Казахтелеком?",
                "Где увидеть скидки и акции для работников Компании?"]
lte_ = ['🛜 Акция "Пилот LTE"', "Об акции", "А как продать?", "Отправить заявку", "Мои продажи"]
pp = ['ALEM PLUS (1 год) c Bereke 2', 'ALEM PLUS (1 год) c Bereke 1', 'ALEM PLUS (без контракта) c Bereke 1',
      'ALEM PLUS (без контракта) c Bereke 2', 'ALEM TV (без контракта)', 'ALEM TV (1 год)',
      'ALEM MOBILE (без контракта) c Bereke 1', 'ALEM MOBILE (без контракта) c Bereke 2',
      'ALEM MOBILE (1 год) c Bereke 1', 'ALEM MOBILE (1 год) c Bereke 2', 'ТП Алем']
faq_1 = {
    'Ha кого направлена программа “Демеу” в AO “Казахтелеком”?':
        'Социальная поддержка Программы «Демеу» AO «Казахтелеком»:  (далее - Программа) направлена '
        'работникам по статусу: \
  \n1) многодетная семья - семья, имеющая в своем составе четырех и более совместно проживающих несовершеннолетних '
        'детей, в том числе детей, обучающихся по очной форме обучения в организациях среднего, \
  технического и профессионального, послесреднего, высшего и (или) послевузовского образования после достижения ими '
        'совершеннолетия до времени окончания образования (но не более чем до достижения \
  двадцатитрехлетнего возраста); '
        '\n2) семья c детьми-инвалидами - семья, имеющая в своем составе ребенка (детей) до восемнадцати лет, '
        'имеющего(-их) нарушение здоровья co стойким расстройством функций организма,\
  обусловленное заболеваниями, увечьями (ранениями, травмами, контузиями), их последствиями, дефектами, которые '
        'приводят к ограничению жизнедеятельности и необходимости ero (их) социальной защиты; \
  \n3) семья, усыновившая/удочерившая более 2-x детей - семья, имеющая в своем составе более 2-x несовершеннолетних '
        'усыновленных/удочеренных детей, которые состоят на диспансерном учете по состоянию здоровья, и '
        'единственного кормильца. \
  \n4) Работникам грейда A8-B4 устанавливается социальная поддержка по оплате выпускного курса обучения (без учета '
        'расходов на проживание и питание) их детей в среднем специальном учебном заведении (далее - CYZ)/высшем '
        'учебном заведении (далее - BYZ). \
  \nBce виды социальной поддержки оказываются работникам Общества, имеющим на момент предоставления социальной '
        'поддержки стаж непрерывной работы в Обществе не менее 3-x лет.\
  \n*Обращения физических лиц ob оказании социальной поддержки/помощи, не состоящих в трудовых отношениях c AO '
        '«Казахтелеком», к рассмотрению не принимаются.',
    'Виды социальной поддержки для работников': '1) Возмещение расходов, связанных c приобретением путевок в детские '
                                                'оздоровительные лагеря; \
  \n2) Возмещение расходов, связанных c приобретением путевок в детские '
                                                'оздоровительные санатории (для детей-инвалидов); \
  \n3) Материальная помощь на приобретение лекарственных средств для детей; \
  \n4) Материальная помощь на питание учащихся школ; \n5) материальная помощь к началу учебного года; \
  \n6) Возмещение средств за медицинскую реабилитацию/индивидуальную программу реабилитации ребенка '
                                                '(для детей-инвалидов); \
  \n7) Возмещение средств за специальные образовательные программы (для детей-инвалидов); \
  \n8) Возмещение средств за посещение специальных коррекционных организаций (для детей-инвалидов); \
  \n9) Материальная помощь выпускникам школ, не достигшим на дату окончания школы совершеннолетия и окончившим учебу '
                                                'на отлично; \
  \n10) Возмещение (работникам грейда A8-B4) расходов по оплате выпускного курса обучения (без учета расходов на '
                                                'проживание и питание) их детей в среднем специальном учебном '
                                                'заведении (далее - CYZ)/высшем учебном заведении '
                                                '(далее - BYZ).',
    'Процесс подачи заявления в социальную комиссию':
        'Основанием для рассмотрения вопроса об оказании социальной поддержки является заявление работника \n'
        'ЦА/филиала, поданное в Социальную комиссию ЦА/филиала с приложением подтверждающих документов.',
    'Где оформлять заявление?': 'Заявление оформляете в своей рабочей базе(БРД). Специальных баз нет.',
    'Председатель социальной комиссии': 'Председатель Социальной комиссии в филиалах - Генеральный директор филиала. '
                                        'В ЦА – Главный директор по операционной эффективности',
}
faq_2 = {
    'Как получить справку c места работы?':
        'Заявку на получение спpaвки c места работы необходимо оформить в Базе «Заявки ОЦО HR». '
        '\nСоздать новый – выбрать наименование Вашего филиала – заявка на выдачу справки с места работы – заполнить '
        'ФИО сотрудника, вид справки и необходимые критерии (язык, стаж, должностной оклад, средняя заработная плата) '
        '– сохранить заявку – Отправить в ОЦО В Заявке автоматически будет указан Исполнитель Вашей заявки.',
    'Как создать учетную запись Lotus и доступ к ИС и БРД?':
        'Для создания учетной записи Lotus Notes необходимо обратиться к Вашему курирующему руководителю'
        '/наставнику/делопроизводителю структурного подразделения для оформления заявки в Базе ЕСУД (Единая система '
        'управления доступом). \nПо мере готовности учетной записи (файл с логином и паролем), необходимо оформить '
        'заявку в Help Desk по номеру: +7 727 2587304 После установления учетной записи Lotus Notes, необходимо '
        'самостоятельно создать заявку в Базе ЕСУД с указанием необходимого для Вас доступа к ИС и БД.',
    'Куда обратиться если забыл пароль или сбой в Lotus?':
        'Оставить заявку HelpDesk +77272587304 по возникшим вопросам.',
    'Как оплачиваются листы временной нетрудоспособности?':
        'Листы временной нетрудоспособности для работников (членов профсоюзной организации и присоединившихся к '
        'Коллективному договору) оплачиваются в зависимости от непрерывного стажа работы в компании: '
        '\n- до 2-х лет включительно - в соответствии с законодательством Республики Казахстан; '
        '\n- до 5 лет - 40% средней заработной платы; '
        '\n- свыше 5 лет - 70% средней заработной платы за дни временной нетрудоспособности.',
    'Кто заполняет больничный лист?':
        'Больничный лист заполняет табельщик/делопроизводитель структурного подразделения. '
        'B больничном листе отражаете  наименование филиала "Дивизион по розничному бизнесу - филиал AO "Казахтелеком" '
        'и свою должность.',
    'Кому сдавать лист временной нетрудоспособности (больничный лист)?':
        'Прежде чем сдать лист временной нетрудоспособности, его необходимо заполнить и подписать  y своего '
        'непосредственного руководителя. \nВ случае, если в Вашем офисе отсутствует работник фронт-офиса ОЦО HR - '
        'отсканировать с двух сторон БЛ и оформить заявкой в Базе Заявки ОЦО HR; в противном случае – сдать заполненный'
        ' оригинал БЛ работнику фронт-офиса ОЦО HR.',
    'Как вступить в Профсоюз?':
        'Для вступления в Локальный профсоюз, необходимо оформить заявление о вступлении в Профсоюз Вашего филиала '
        '(шаблон о вступлении в Профсоюз можно получить у работника фронт-офиса ОЦО HR) и оформить заявку в Базе Заявки'
        ' в ОЦО ЗП об удержании профсоюзных взносов. Процент удержания составляет – 1 %.',
    'Страховка по ДМС (добровольное медицинское страхование)':
        'Страховка по ДМС (добровольное медицинское страхование) осуществляется  работникам имеющих стаж работы в '
        'Обществе более 3-x  лет, при условии возможности страхового покрытия',
    'Где найти телефон коллег?':
        'Телефон коллеги Вы можете найти базе "Телефонный справочник Общества" - номера телефонов по Фамилии, поиск '
        'сотрудников по подразделению',
    'Обходной лист. Когда ero оформлять?':
        '1) При оформление заявления на увольнение, автоматически сформирован в третьем листе обходной лист и '
        'указаны подписанты.'
        '\n2) При переводе/одностороннем порядке/ в филиал обходной лист оформляем в своих рабочих базах',
}
faq_procurement_portal = {
    'Не могу войти на сайт': 'Возможно Вы ввели некоректный адрес. Вам нужно ввести в адресную строку следующий адрес: '
                             'zakup.telecom.kz/app ',
    'Какие логин и пароль нужно ввести для входа?': 'Логин и пароль такие же как на mail.telecom.kz, '
                                                    'CheckPoint или при входе в Ваш ПК',
    'Логин и пароль корректный, но все равно не удалось войти': '"Возможно Вы еще не зарегистрированы на портале '
                                                                'закупок. Для регистрации Вам нужно обратититься к '
                                                                'одному из специалитов технической поддержки портала '
                                                                'закупок. Для обращения Вы можете перейти главное меню '
                                                                'ktbot и оставить Ваше обращения в разделе '
                                                                '""У меня есть вопрос""."',
    'Не могу зайти на сайт хотя ввожу адрес сайта верно': 'Возможно у вас проблемы с интернетом или не подключили '
                                                          'CheckPoint(если входите через ноутбук)'
}
faq_procurement_activities = {
    'Чем регулируются закупки в АО «Казахтелеком»?':
        'Порядок осуществления закупок акционерным обществом «Фонд национального благосостояния «Самрук-Қазына» '
        'и юридическими лицами, пятьдесят и более процентов голосующих акций (долей участия) которых прямо или косвенно'
        ' принадлежат АО «Самрук-Қазына» на праве собственности или доверительного управления и Регламент '
        'взаимодействия Дирекции «Телеком Комплект» с филиалами АО «Казахтелеком».',
    'Как определяется способ закупа и какие виды закупок?':
        """1) тендер: 
- двухэтапный 
- с торгами на понижение (на усмотрение Заказчика, нельзя по СМР, экспертизе, тех.надзору) 
- с ограниченным участием (после 2 несост.тендеров) 
2) запрос ценовых предложений – до 10 000 МРП (обязателен при закупке товаров по реестру доверенного ПО и продукции эл.промышленности и товаров «экономики простых вещей» без ограничений по сумме подлежит исключению с 1 января 2024 года);
3) через товарные биржи; 
4) из одного источника (соответствие с ст. 59 Порядка); 
5) посредством электронного магазина – до 8 млн.тг по 32 категориям товаров на площадке skstore.kz.
6) особый порядок (соответствие с ст. 73 Порядка)""",
    'Какие виды плана закупок существуют в компании?':
        'План закупок (предварительный, годовой, долгосрочный) - документ, содержащий сведения о закупке товаров, '
        'работ, услуг, необходимых для удовлетворения нужд заказчика в течение периода, определённого планом и в '
        'соответствии с графиком плана. ',
    'Что такое демпинг и как применяется в закупках?': """
Демпинг - продажа товаров и услуг по искусственно заниженным ценам, ниже рыночных. 
Ценовое предложение признаётся демпинговым в следующих случаях: 
- ценовое предложение на СМР, комплексные работы по которым имеется сметная, предпроектная, проектная 
(проектно-сметная) документация, утвержденная в установленном порядке, более чем на 5% ниже плановой суммы предпроектные
- проектные и изыскательские работы, работ по комплексной вневедомственной экспертизе проектов строительства и услуг по техническому надзору за строительством объектов более чем на 10% ниже плановой суммы; 
- ценовое предложение на консультационные (консалтинговые) услуги более чем на 70 % ниже среднеарифметической цены всех представленных ценовых предложений; • ценовое предложение на иные работы, услуги более чем на 20 % ниже среднеарифметической цены всех представленных ценовых предложений
- ценовое предложение на товары более чем на 15% ниже плановой суммы.
Антидемпинговые условия не распространяются на закупки с торгами на понижение и тендера по ЗКС (с переговорами на понижение цены)."
    """,
    'Что такое офтейк контракт и как заключается?':
        """
Офтейк-контракт — это гарантия для казахстанских товаропроизводителей на долгосрочный заказ, с учетом организации производства, реализуется в рамках программы импортозамещения.
Для приобретения товара, производимого потенциальным поставщиком в рамках реализации Проекта по созданию новых производств, посредством заключения офтейк-контракта, проводится закупка способом из одного источника на основании пп.8 п.1 Ст.59 Порядка осуществления закупок. 
        """,
    'Что такое пул товаров импортозамещения?':
        'Пул товаров всех ПК Фонда, в которых имеется постоянная и стабильная востребованность группы компаний, но '
        'отсутствует производство в стране.',
    'Как определяется маркетинговая цена?':
        'Маркетинговая цена - цена на товар, применяемая заказчиком для формирования бюджетов расходов/плана(ов) '
        'закупок и не включающая в себя налог на добавленную стоимость. Маркетинговые цены на товары определяются в '
        'соответствии с Приложением № 3 к Порядку."'
}
branches = ['Центральный Аппарат', 'Объединение Дивизион "Сеть"', 'Дивизион по Розничному Бизнесу',
            'Дивизион по Корпоративному Бизнесу', 'Корпоративный Университет', 'Дивизион Информационных Технологий',
            'Дирекция Телеком Комплект', 'Дирекция Управления Проектами', 'Сервисная Фабрика']

# branches_admin = [
#     {'branch': 'Центральный Аппарат', 'sapa_admin': '353845928'},
#     {'branch': 'Обьединение Дивизион "Сеть"', 'sapa_admin': '353845928'},
#     {'branch': 'Дивизион по Розничному Бизнесу', 'sapa_admin': '353845928'},
#     {'branch': 'Дивизион по Корпоративному Бизнесу', 'sapa_admin': '353845928'},
#     {'branch': 'Корпоративный Университет', 'sapa_admin': '1066191569'},
#     {'branch': 'Дивизион Информационных Технологий', 'sapa_admin': '353845928'},
#     {'branch': 'Дирекция Телеком Комплект', 'sapa_admin': '353845928'},
#     {'branch': 'Дирекция Управления Проектами', 'sapa_admin': '353845928'},
#     {'branch': 'Сервисная Фабрика', 'sapa_admin': '353845928'}
# ]


# branches_admin = [
#      # {'branch': 'Центральный Аппарат', 'sapa_admin': '735766161'},
#      {'branch': 'Центральный Аппарат', 'sapa_admin': '559872057'},
#      # {'branch': 'Центральный Аппарат', 'sapa_admin': '1009867354'},
#      # {'branch': 'Центральный Аппарат', 'sapa_admin': '1066191569'},
#      # {'branch': 'Обьединение Дивизион "Сеть"', 'sapa_admin': '1621516433'},
#      {'branch': 'Обьединение Дивизион "Сеть"', 'sapa_admin': '735766161'},
#      {'branch': 'Дивизион по Розничному Бизнесу', 'sapa_admin': '531622371'},
#      {'branch': 'Дивизион по Корпоративному Бизнесу', 'sapa_admin': '468270698'},
#      # {'branch': 'Корпоративный Университет', 'sapa_admin': '476878708'},
#      {'branch': 'Корпоративный Университет', 'sapa_admin': '1066191569'},
#      # {'branch': 'Корпоративный Университет', 'sapa_admin': '353845928'},
#      {'branch': 'Дивизион Информационных Технологий', 'sapa_admin': '577247261'},
#      {'branch': 'Дирекция Телеком Комплект', 'sapa_admin': '597334185'},
#      {'branch': 'Дирекция Управления Проектами', 'sapa_admin': '947621727'},
#      {'branch': 'Сервисная Фабрика', 'sapa_admin': '477945972'}
# ]

branches_admin = 735766161
# branches_admin = 1066191569

def get_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    if check_id(str(message.chat.id)):
        markup.add(types.KeyboardButton("Админ панель"))
    #button1 = types.KeyboardButton(hse_competition_field[0])
    #button2 = types.KeyboardButton("🚀Цифровой марафон | Регистрация")
    #button2 = types.KeyboardButton('💸Регистрация на обучение "Финансовая грамотность"')
    button9 = types.KeyboardButton("📄Подтверждение сдачи декларации")
    button10 = types.KeyboardButton('📶SAPA+')
    button = types.KeyboardButton("😊Welcome курс | Адаптация")
    button3 = types.KeyboardButton("🗃️База знаний")
    button4 = types.KeyboardButton("👷Заполнить карточку БиОТ")
    button5 = types.KeyboardButton("📄У меня есть вопрос")
    button6 = types.KeyboardButton("🧐Мой профиль")
    button7 = types.KeyboardButton('🖥Портал "Бірлік"')
    button8 = types.KeyboardButton(lte_[0])
    markup.add(button10, button9, button)
    if get_branch(message.chat.id) == branches[2]:
        markup.add(button8)
    markup.add(button3, button7, button5, button4, button6)
    return markup

def send_welcome_message(bot, message):
    welcome_message = f'Привет, {get_firstname(message)} 👋'
    markup = get_markup(message)
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    send_photo_(bot, message.chat.id, "images/menu.jpg")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "B моем сценарии есть несколько команд:\
        \n/menu — вернуться в главное меню (ты можешь сделать это в любой момент прохождения демо!)\
        \n/help — связаться c разработчиками (используй эту команду, если столкнешься c трудностями "
                                      "или y тебя есть предложения для улучшения)\
    \n/start — Перезапустить бота \
    \n/language - Сменить язык бота\
    \n\nKoмaнды ты можешь найти во вкладке «Меню» в строке сообщений (слева внизу) или просто пришли название команды, "
                                      "только значок «/» не забывай!")


regions_ = ["город Астана", "город Алматы", "город Шымкент", "город Актобе", "Карагандинская область",
            "Абайская область", "Акмолинская область", "Актюбинская область", "город Караганда",
            "Алматинская область", "Атырауская область", "Западно-Казахстанская область", "Жамбылская область",
            "Жетысуская область", "Костанайская область", "Кызылординская область", "Мангистауская область",
            "Павлодарская область", "Северо-Казахстанская область", "Туркестанская область", "Улытауская область",
            "Восточно-Казахстанская область"]


def send_error(bot, message):
    common_file.send_photo_(bot, message.chat.id, 'images/oops_error.jpg')
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Упс, что-то пошло не так...\nПoжaлyйcтa, попробуйте заново запустить бота нажав кнопку /menu")


def check_is_command(bot, message, text_):
    if text_ == "/start":
        send_welcome_message(bot, message)
        return True
    elif text_ == "/menu" or text_ == "/help" or text_ == "/language":
        menu(bot, message)
        return True
    return False

def fin_gram(bot, message, message_text):
    user_id = message.chat.id
    if message_text == '💸Регистрация на обучение "Финансовая грамотность"':
        # Проверяем статус пользователя
        is_verified = get_user_verification_status_reg(user_id)
        #bot.send_message(user_id, str(check_if_registered(user_id)))
        #bot.send_message(user_id, str(check_registration_message_in_history(user_id)))
        add_message_to_history(user_id, message_text)

        if not is_verified:
            # Если пользователь не верифицирован, просим ввести корпоративную почту
            msg = bot.send_message(user_id, "Необходимо подтвердить вашу корпоративную электронную почту, "
                                            "на которую будет отправлен 4-значный код для верификации. "
                                            "\nВведите вашу электронную почту. \nПример: User.U@telecom.kz" )
            bot.register_next_step_handler(msg, process_email, bot)
        elif check_registration_message_in_history(user_id) and check_if_registered(user_id):
            # Создаем клавиатуру с кнопками "Да" и "Нет"
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            yes_button = types.KeyboardButton('Да')
            no_button = types.KeyboardButton('Нет')
            markup.add(yes_button, no_button)

            # Запрашиваем подтверждение участия в обучении
            msg = bot.send_message(user_id, "Вы уже зарегистрированы на это обучение, желаете удалить запись?",
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, delete_fin_gram, bot)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            yes_button = types.KeyboardButton('Да')
            no_button = types.KeyboardButton('Нет')
            markup.add(yes_button, no_button)

            # Запрашиваем подтверждение участия в обучении
            msg = bot.send_message(user_id, "Вы подтверждаете что желаете учавствовать в обучении?",
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, confirm_fin_gram, bot)


def delete_fin_gram(message, bot):
    user_id = message.chat.id
    response = message.text.strip().lower()

    if response == 'да':
        delete_participation(message)
        delete_registration_message_in_history(user_id)
        clear_message_history(user_id)

        # Отправляем сообщение о успешном удалении
        bot.send_message(user_id, "Вы были удалены из обучения")
        menu(bot, message)

    elif response == 'нет':
        # Отправляем сообщение об отмене регистрации и возвращаем в главное меню
        bot.send_message(user_id, "Удаление отменено.")
        menu(bot, message)
    else:
        # Обработка неверного ввода, если вдруг пришел текст не "Да" и не "Нет"
        msg = bot.send_message(user_id, "Пожалуйста, выберите 'Да' или 'Нет'.")
        bot.register_next_step_handler(msg, confirm_fin_gram, bot)


def confirm_fin_gram(message, bot):
    user_id = message.chat.id
    response = message.text.strip().lower()
    if response == 'да':
        # Добавляем запись в таблицу financial_literacy
        webinar_name = "Финансовая грамотность"
        sql_query = "INSERT INTO financial_literacy (user_id, webinar_name) VALUES (%s, %s)"
        params = (user_id, webinar_name)
        db_connect.execute_set_sql_query(sql_query, params)

        # Отправляем сообщение о успешной регистрации
        bot.send_message(user_id, "Вы успешно зарегистрировались на обучение по финансовой грамотности!")
        bot.send_message(user_id, "Ссылка на вебинар 08.09.2024 в 10:00 по аст.времени \nТема: Финансовая Грамотность для КазахТелеком\nВремя: 11 сент. 2024 10:00  Алматы \nВойти "
                                  "Zoom Конференция: \nhttps://us02web.zoom.us/j/86082733518?pwd=XZmACbDsdC6PtqopaseSM5hhFhZCp5.1 \n\nИдентификатор конференции: "
                                  "860 8273 3518 \nКод доступа: 11", protect_content=True)
        menu(bot, message)
    elif response == 'нет':
        # Отправляем сообщение об отмене регистрации и возвращаем в главное меню
        bot.send_message(user_id, "Регистрация отменена.")
        menu(bot, message)
    else:
        # Обработка неверного ввода, если вдруг пришел текст не "Да" и не "Нет"
        msg = bot.send_message(user_id, "Пожалуйста, выберите 'Да' или 'Нет'.")
        bot.register_next_step_handler(msg, confirm_fin_gram, bot)


def verification(bot, message, message_text):
    user_id = message.chat.id
    if message_text == "📄Подтверждение сдачи декларации":
        add_message_to_history(user_id, message_text)
        bot.send_message(user_id, "Нажимая на эту кнопку, подтверждаете, что вами, декларация по форме "
                                  "налоговой отчетности 270.00, была сдана")
        # Создаем кнопки для ответа
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        yes_button = types.KeyboardButton('Да')
        no_button = types.KeyboardButton('Нет')
        markup.add(yes_button, no_button)

        # Проверяем статус верификации
        is_verified = get_user_verification_status_reg(user_id)
        is_verified_decl = get_user_verification_status(user_id)
        # bot.send_message(message.chat.id, str(is_verified))
        # bot.send_message(message.chat.id, str(is_verified_decl))
        # bot.send_message(message.chat.id, str(check_registration_message_in_history_decl))
        # В зависимости от статуса отправляем подтверждение или запрос на почту
        if not is_verified:
            # Если пользователь не верифицирован, запрашиваем почту
            msg = bot.send_message(user_id,
                                   "Необходимо подтвердить вашу корпоративную электронную почту, на которую будет отправлен 4-значный код для верификации. \nВведите вашу электронную почту. \nПример: User.U@telecom.kz")
            bot.register_next_step_handler(msg, process_email, bot)
        elif not is_verified_decl and check_registration_message_in_history_decl(user_id):
            # Запрашиваем подтверждение декларации (Да/Нет)
            msg = bot.send_message(user_id, "Подтверждаете ли вы сдачу декларации?", reply_markup=markup)
            bot.register_next_step_handler(msg, process_declaration_confirmation, bot)

        else:
            # Если пользователь уже подтвердил декларацию
            bot.send_message(user_id, "Вы уже верифицировали свою почту и подтвердили подписание декларации.")
            menu(bot, message)


# Функция для обработки ответа (Да/Нет) по декларации
def process_declaration_confirmation(message, bot):
    user_id = str(message.chat.id)
    response = message.text.strip().lower()  # Приводим ответ к нижнему регистру для проверки

    if response == 'да':
        # Если ответ "Да", обновляем статус в базе данных
        sql_query = "UPDATE users SET is_verified_decl = TRUE WHERE id = %s"
        params = (user_id,)

        try:
            # Выполняем SQL-запрос
            db_connect.execute_set_sql_query(sql_query, params)
            bot.send_message(user_id, "Подтверждение сдачи декларации успешно завершено!")

            # Отправляем меню после успешного обновления
            menu(bot, message)

        except Exception as e:
            # Ловим возможные ошибки и выводим их для отладки
            bot.send_message(user_id, f"Произошла ошибка при обновлении статуса: {e}")

    elif response == 'нет':
        # Если ответ "Нет", возвращаем пользователя в главное меню
        bot.send_message(user_id, "Вы отменили подтверждение декларации.")
        menu(bot, message)

    else:
        # Если введен некорректный ответ, просим повторить
        msg =bot.send_message(user_id, "Пожалуйста, выберите один из вариантов: 'Да' или 'Нет'.")
        bot.register_next_step_handler(msg, process_declaration_confirmation, bot)


def process_email(message, bot):
    user_id = str(message.chat.id)
    regex = r'\b[A-Za-z0-9._%+-]+@telecom.kz\b'
    # Получаем email пользователя из сообщения
    email = message.text
    set_email(message, email)

    if email.startswith('/'):
        # Удаляем таймер, если он есть
        verification_timers.pop(user_id, None)
        # Переход в меню, если команда "/menu"
        if email == '/menu':
            menu(bot, message)
            return True
    if email:
        # Проверка на корпоративный email
        if re.fullmatch(regex, email):
            # Отправляем код подтверждения на email пользователя, передаем bot и chat_id
            send_verification_code(user_id, bot, message)
            msg = bot.send_message(message.chat.id,
                                   f"Для подтверждения, пожалуйста, введите код, отправленный на вашу рабочую почту в течении 5 минут. \n\nВводя отправленный вам код, вы даете согласие на сбор и обработку персональных данных")
            bot.register_next_step_handler(msg, verify_code, bot)
        else:
            # Если email не корпоративный, уведомляем пользователя и повторно запрашиваем email
            msg = bot.send_message(message.chat.id,
                                   "Введённый адрес электронной почты не является корпоративным. Просим Вас ввести корректный корпоративный E-mail еще раз.")
            bot.register_next_step_handler(msg, process_email, bot)
    else:
        bot.send_message(message.chat.id,
                         "Не удалось найти вашу почту. Пожалуйста, убедитесь, что вы ввели правильный email.")


def start_verification_timer(user_id, bot, message):
    # Таймер на 5 минут (300 секунд)
    def timer():
        time.sleep(300)  # Ожидание 5 минут
        if user_id in verification_timers:
            del verification_timers[user_id]  # Удаляем таймер по истечению времени
            sql_query = "UPDATE users SET email = NULL WHERE id = %s"
            params = (user_id,)
            db_connect.execute_set_sql_query(sql_query, params)
            bot.send_message(message.chat.id, "Время ожидания истекло.")
            msg = bot.send_message(message.chat.id, "Введите ваш корпоративный E-mail:")
            bot.register_next_step_handler(msg, process_email, bot)
            return

    # Создаем и запускаем поток для таймера
    verification_timers[user_id] = threading.Thread(target=timer)
    verification_timers[user_id].start()


def sapa_con(bot, message):
    user_id = message.chat.id
    message_text = message.text

    if message_text == '📶SAPA+':
        # Меню с четырьмя дополнительными кнопками
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Инструкции'))
        markup.add(types.KeyboardButton('Пункты выдачи роутеров SAPA+'))
        markup.add(types.KeyboardButton('SAPA+QUEST'))
        # markup.add(types.KeyboardButton('Чат бот по техническим вопросам/ОДС'))SAPA+QUEST
        markup.add(types.KeyboardButton('Верификация абонентов SAPA+'), types.KeyboardButton('Тех поддержка SAPA+ для мегалайнеров'))
        # markup.add(types.KeyboardButton('Помощь по настройке/скорости SAPA+ ДТПК'), types.KeyboardButton('Верификация абонентов SAPA+'))

        bot.send_message(user_id, "Выберите необходимую категорию:", reply_markup=markup)
        bot.register_next_step_handler(message, additional_info_handler, bot)

    else:
        # Если пользователь ввел что-то другое, попросим сделать выбор снова
        bot.send_message(user_id, "Пожалуйста, выберите действие из предложенных вариантов.")
        bot.register_next_step_handler(message, sapa_con, bot)

def sapa_instruments(message, bot):
    user_id = str(message.chat.id)
    response = message.text.strip().lower()

    if response.startswith('/'):
        # Переход в меню, если команда "/menu"
        if response == '/menu':
            menu(bot, message)
            return True
    elif response == 'таблица лидеров':
        display_leaderboard(bot, message)
    elif response == 'оценка ссылок' and str(user_id) in sapa_admin:
        show_pending_links(message, bot)
    elif response == 'загрузить таблицу' and str(user_id) in sapa_admin:
        # msg = bot.send_message(user_id, "Пожалуйста, загрузите Excel файл с данными участников.")
        # bot.register_next_step_handler(msg, upload_sapa_table, bot)
        bot.send_message(message.chat.id, "Еще в разработке")
        bot.send_message(message.chat.id, "Пожалуйста вернитесь в главное меню. Написав команду '/menu'")
    elif response == 'загрузить ссылку/фото':
        msg = bot.send_message(user_id, "Пожалуйста отправьте ссылку/фото:")
        bot.register_next_step_handler(msg, upload_link, bot)
    elif response == 'назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            # types.KeyboardButton('Бонусная система SAPA+'),
                   types.KeyboardButton('Инструкции, техническая поддержка и точки передачи'))

        msg = bot.send_message(user_id, "Выберите один из вариантов", reply_markup=markup)
        bot.register_next_step_handler(msg, sapa_con, bot)
    else:
        bot.send_message(user_id, "Пожалуйста, выберите один из вариантов.")
        bot.register_next_step_handler(message, sapa_instruments, bot)

def additional_info_handler(message, bot):
    user_id = message.chat.id
    info_request = message.text.strip().lower()

    # Обработка кнопок "необходимая информация"
    if info_request.startswith('/'):
        if info_request == '/menu':
            menu(bot, message)
            return True
    elif info_request == 'инструкции':
        bot.send_message(user_id, "Видеоинструкция по настройке роутера:\nhttps://youtu.be/rgvRczmW6Ng")
        bot.send_message(user_id, "Инструкция для мегалайнера. Помощь в установке роутера для абонента https://youtu.be/0e4Yc5Kdzpo")
        bot.send_document(user_id, open("files/Инструкция_по_подключению_и_настройке_роутера.pdf", 'rb'))
        bot.send_document(user_id, open("files/Создание_заявки_мегалайнером+смс_6_тизначный.pdf", 'rb'))
        bot.send_document(user_id, open("files/Создание заявки мегалайнером.pdf", 'rb'))
        bot.send_document(user_id, open("files/Инструкция_пользователя_WFM_инсталлятор.pdf", 'rb'))
        bot.send_document(user_id, open("files/Инструкция_Передача оборудования SAPA+.pdf", 'rb'))
        bot.send_photo(
            chat_id=user_id,  # ID пользователя
            photo=open("images/Памятка.jpeg", 'rb'),  # Путь к изображению
            caption=(
                'Если вы столкнулись с ситуацией, что абоненту по той или иной причине не пришло push-уведомление, '
                'то для начала нужно выполнить действия, описанные в документе.\n\n'
                'Также у всех есть возможность повторно отправить push-уведомление. Требуется немного подождать. '
                'Не всегда они приходят моментально.\n\n'
                'После того как все выше указанные действия не помогли, попросить абонента заново авторизоваться '
                'в мобильном приложении.\n\n'
                'Только после всех этих действий, подавать заявку в группу.'
            )
        )

        bot.send_photo(
            chat_id=user_id,
            photo=open("images/5303249485243213412.jpg", 'rb'),
            caption=(
                '<b>Инструкция в случае, если абонент НЕ сообщил 4-х значный код Мегалайнеру и закрыл мобильное приложение:</b>\n'
                '1. Абоненту необходимо повторно открыть мобильное приложение и авторизоваться\n'
                '2. Внизу экрана нажать на раздел «Чаты»\n'
                '3. После перехода в раздел «Чаты», в правом верхнем углу нажать на «Колокольчик». '
                'Откроется центр нотификации (список с PUSH уведомлениями)\n'
                '4. Нажать на сообщение с кодом, которым ранее абонент подписал Акт приема-передачи оборудования\n'
                '5. Откроется экран «Установка роутера выполнена успешно» и внизу под текстом будет продублирован 4-х значный код для Мегалайнера.'
            ),
        )
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'пункты выдачи роутеров sapa+':
        bot.send_document(user_id, open("files/Пункты_выдачи_и_обучение_мегалайнеров_SAPAplus.pdf", 'rb'))
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'чат бот по техническим вопросам/одс':
        bot.send_message(user_id, "Ссылка для подключению к боту: https://t.me/C_M_S_bot")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'тех поддержка sapa+ для мегалайнеров':
        bot.send_message(user_id, "Ссылка для присоединения к группе: https://t.me/+gCyDTZGRZIBlZDIy")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'sapa+quest':
        bot.send_message(user_id, "Cсылка на информационый канал: https://t.me/+LJl92t3A3NE2MzMy")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'помощь по настройке/скорости sapa+ дтпк':
        bot.send_message(user_id, "Ссылка для присоединения к группе: https://t.me/+yVOT2YdR6hAyMjRi")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'верификация абонентов sapa+':
        bot.send_message(user_id, "Вопросы по личному кабинету Мегалайнера связанные с доступом (не пришло СМС, удалил СМС, сменить привязку к Филиалу) - 👉 нажмите сюда")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    else:
        bot.send_message(user_id, "Пожалуйста, выберите один из вариантов.")
        bot.register_next_step_handler(message, additional_info_handler, bot)

def links_instruments(message, bot):
    user_id = str(message.chat.id)
    response = message.text.strip().lower()

    if response.startswith('/'):
        # Переход в меню, если команда "/menu"
        if response == '/menu':
            menu(bot, message)
            return True
    elif response == 'загрузить':
        msg = bot.send_message(user_id, "Пожалуйста отправьте ссылку/фото:")
        bot.register_next_step_handler(msg, upload_link, bot)
    elif response == 'список непроверенных ссылок':
        show_user_links(bot, message)
    else:
        bot.send_message(user_id, "Пожалуйста, выберите один из вариантов.")
        bot.register_next_step_handler(message, links_instruments, bot)


def upload_link(message, bot):
    user_id = message.chat.id

    # Проверка, есть ли текст в сообщении
    if message.text:
        link = message.text.strip()

        if link.startswith('/'):
            if link == '/menu':
                menu(bot, message)
                return True
        elif link.lower() == 'стоп':
            bot.send_message(user_id, "Процесс загрузки ссылок завершён.")
            msg = bot.send_message(user_id, "Выберите один из доступных вариантов ниже:")
            bot.register_next_step_handler(msg, links_instruments, bot)
            return

        if not link.startswith("http"):
            bot.send_message(user_id, "Неверный формат ссылки. Пожалуйста, укажите корректный URL.")
            msg = bot.send_message(user_id, "Пожалуйста, отправьте ссылку/фото:")
            bot.register_next_step_handler(msg, upload_link, bot)
            return

        try:
            user_info = get_user(message.chat.id)
            email = user_info[6]
            branch = user_info[7]
            if not email or not branch:
                bot.send_message(user_id, "Ошибка: email или филиал не найден.")
                return

            # Сохранение ссылки с актуальной датой и branch пользователя
            db_connect.execute_set_sql_query("""
                INSERT INTO sapa_link (email, link, is_checked, status, branch, date) 
                VALUES (%s, %s, FALSE, NULL, %s, NOW())
            """, (email, link, branch))

            # Проверяем и добавляем пользователя в sapa_bonus, если его нет
            check_user_query = "SELECT * FROM sapa_bonus WHERE email = %s"
            result = db_connect.execute_get_sql_query(check_user_query, (email,))

            if not result:
                user_query = "SELECT firstname, lastname FROM users WHERE email = %s"
                user_info = db_connect.execute_get_sql_query(user_query, (email,))
                if user_info:
                    firstname, lastname = user_info[0]
                    fullname = f"{firstname} {lastname}"
                    db_connect.execute_set_sql_query("""
                        INSERT INTO sapa_bonus (email, fullname, bonus_score, total_score)
                        VALUES (%s, %s, 0, 0)
                    """, (email, fullname))

            bot.send_message(user_id, "Ссылка успешно загружена! Ожидайте проверки.")

            bot.send_message(user_id, "Вы будете перенаправлены в главное меню SAPA+")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(
                # types.KeyboardButton('бонусная система SAPA+'),
                       types.KeyboardButton('Инструкции, техническая поддержка и точки передачи'))

            msg = bot.send_message(user_id, "Выберите одно из действий:", reply_markup=markup)
            bot.register_next_step_handler(msg, sapa_con, bot)
        except Exception as e:
            bot.send_message(user_id, f"Произошла ошибка при загрузке ссылки: {e}")

    # Обработка фото
    elif message.photo:
        bot.send_message(user_id, "Фото получено, начинаем загрузку...")
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            file_url = f'https://api.telegram.org/file/bot{db_connect.TOKEN}/{file_info.file_path}'

            response = requests.get(file_url)
            if response.status_code == 200:
                file_data = response.content
            else:
                bot.send_message(user_id, "Ошибка при загрузке фото. Попробуйте снова.")
                return

            user_info = get_user(message.chat.id)
            email = user_info[6]
            branch = user_info[7]
            if not email or not branch:
                bot.send_message(user_id, "Ошибка: email или филиал не найден.")
                return

            # Сохранение фото с актуальной датой и branch пользователя
            db_connect.execute_set_sql_query("""
                INSERT INTO sapa_link (email, link, is_checked, status, image_data, branch, date) 
                VALUES (%s, NULL, FALSE, NULL, %s, %s, NOW())
            """, (email, file_data, branch))

            check_user_query = "SELECT * FROM sapa_bonus WHERE email = %s"
            result = db_connect.execute_get_sql_query(check_user_query, (email,))

            if not result:
                user_query = "SELECT firstname, lastname FROM users WHERE email = %s"
                user_info = db_connect.execute_get_sql_query(user_query, (email,))
                if user_info:
                    firstname, lastname = user_info[0]
                    fullname = f"{firstname} {lastname}"
                    db_connect.execute_set_sql_query("""
                        INSERT INTO sapa_bonus (email, fullname, bonus_score, total_score)
                        VALUES (%s, %s, 0, 0)
                    """, (email, fullname))

            bot.send_message(user_id, "Фото успешно загружено и ожидает проверки.")

            bot.send_message(user_id, "Вы будете перенаправлены в главное меню SAPA+")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(
                # types.KeyboardButton('бонусная система SAPA+'),
                       types.KeyboardButton('Инструкции, техническая поддержка и точки передачи'))

            msg = bot.send_message(user_id, "Выберите одно из действий:", reply_markup=markup)
            bot.register_next_step_handler(msg, sapa_con, bot)

        except Exception as e:
            bot.send_message(user_id, f"Произошла ошибка при загрузке фотографии: {e}")
    else:
        bot.send_message(user_id, "Пожалуйста, отправьте ссылку или фото.")
        bot.register_next_step_handler(message, upload_link, bot)

def get_user_email(user_id):
    # Ensure params is a tuple to avoid SQL errors
    sql_query = """
        SELECT email 
        FROM users 
        WHERE id = %s
    """
    params = (str(user_id),)

    # Execute query and fetch email
    result = db_connect.execute_get_sql_query(sql_query, params)

    # If a result is found, return email
    return result[0][0] if result else None

def show_user_links(bot, message):
    user_info = get_user(message.chat.id)
    user_email = user_info[6]
    if not user_email:
        bot.send_message(message.chat.id, "Ваш email не найден.")
        return

    links_result = db_connect.execute_get_sql_query(
        "SELECT link, status FROM sapa_link WHERE email = %s AND is_checked = FALSE", (user_email,)
    )

    if links_result:
        response_message = "Ваши ссылки и их статусы:\n"
        for link, status in links_result:
            response_message += f"Ссылка: {link}\nСтатус: {status}\n\n"

        bot.send_message(message.chat.id, response_message)
        bot.send_message(message.chat.id, "Вы будете перенаправлены в главное меню SAPA+")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(
            # types.KeyboardButton('бонусная система SAPA+'),
                   types.KeyboardButton('Инструкции, техническая поддержка и точки передачи'))

        msg = bot.send_message(message.chat.id, "Выберите одно из действий:", reply_markup=markup)
        bot.register_next_step_handler(msg, sapa_con, bot)
    else:
        msg = bot.send_message(message.chat.id, "На данный момент у вас нет ссылок, ожидающих проверки.")
        bot.register_next_step_handler(msg, sapa_instruments, bot)


def display_leaderboard(bot, message):
    # Запрос на получение fullname и общего балла, сортировка по общему баллу
    result = db_connect.execute_get_sql_query("""
            SELECT sb.fullname, COALESCE(s.score, 0) + sb.bonus_score AS total_score
            FROM sapa_bonus sb
            LEFT JOIN sapa s ON sb.email = s.email
            ORDER BY total_score DESC
            LIMIT 10
        """)

    # Формируем текст для таблицы лидеров
    leaderboard = "Таблица лидеров:\n" + "\n".join(
        f"{i}. Пользователь: {row[0]} - Общий балл: {row[1]}"
        for i, row in enumerate(result, 1)
    )
    bot.send_message(message.chat.id, leaderboard)

    # Получаем email пользователя на основе их chat ID
    user_email_result = db_connect.execute_get_sql_query(
        "SELECT email FROM users WHERE id = %s",
        (str(message.chat.id),)
    )

    # Проверяем, был ли найден email
    if user_email_result:
        user_email = user_email_result[0][0].strip().lower()  # Нормализуем email в нижний регистр

        # Находим ранг и балл пользователя в таблице лидеров
        user_rank_result = db_connect.execute_get_sql_query("""
                WITH RankedUsers AS (
                    SELECT 
                        sb.email,
                        COALESCE(s.score, 0) + sb.bonus_score AS total_score,
                        ROW_NUMBER() OVER (ORDER BY COALESCE(s.score, 0) + sb.bonus_score DESC) AS rank
                    FROM sapa_bonus sb
                    LEFT JOIN sapa s ON sb.email = s.email
                )
                SELECT rank, total_score
                FROM RankedUsers
                WHERE LOWER(email) = %s  -- Сравнение без учета регистра
            """, (user_email,))

        if user_rank_result:
            user_rank, user_score = user_rank_result[0]
            bot.send_message(message.chat.id, f"Ваше место: {user_rank}, Общий балл: {user_score}")
        else:
            bot.send_message(message.chat.id, "Вы пока не участвуете в конкурсе.")
    else:
        bot.send_message(message.chat.id, "Не удалось найти ваш email.")

    # Переход к доступным опциям
    bot.send_message(message.chat.id, "Перенаправляем вас в главное меню SAPA+")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(
        # types.KeyboardButton('бонусная система SAPA+'),
               types.KeyboardButton('Инструкции, техническая поддержка и точки передачи'))

    msg = bot.send_message(message.chat.id, "Выберите одно из действий:", reply_markup=markup)
    bot.register_next_step_handler(msg, sapa_con, bot)

# Функция для отображения ссылок для администратора с фильтрацией по branch
def show_pending_links(message, bot):
    try:
        if message.chat.id != branches_admin:
            bot.send_message(message.chat.id, "Ошибка: филиал администратора не найден.")
            return

        # Fetch links associated with the admin's branch, not the user's current branch
        result = db_connect.execute_get_sql_query("""
            SELECT id, link, image_data 
            FROM sapa_link 
            WHERE is_checked = FALSE 
            ORDER BY id 
            LIMIT 1
        """)

        if result:
            for row in result:
                link_id, link, image_data = row
                if link:
                    bot.send_message(message.chat.id, f"Ссылка: {link}")
                elif image_data:
                    bot.send_photo(message.chat.id, image_data)

                # Inline keyboard for rating actions
                markup = types.InlineKeyboardMarkup(row_width=2)
                buttons = [
                    types.InlineKeyboardButton("Пост/сторис работника", callback_data=f'пост {link_id}'),
                    types.InlineKeyboardButton("Пост/сторис клиента", callback_data=f'пост1 {link_id}'),
                    types.InlineKeyboardButton("Отзыв", callback_data=f'отзыв {link_id}'),
                    types.InlineKeyboardButton("Ничего", callback_data=f'ничего {link_id}')
                ]
                markup.add(*buttons)

                bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "На данный момент нет новых ссылок или фото для проверки.")
            msg = bot.send_message(message.chat.id, "Выберите один из доступных вариантов ниже:")
            bot.register_next_step_handler(msg, sapa_instruments, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при получении ссылок: {e}")

# Функция для загрузки таблицы участников
# def upload_sapa_table(message, bot):
#     user_id = str(message.chat.id)
#     if message.content_type == 'document':
#         file_info = bot.get_file(message.document.file_id)
#         downloaded_file = bot.download_file(file_info.file_path)
#
#         try:
#             # Загружаем данные из Excel файла в DataFrame
#             df = pd.read_excel(io.BytesIO(downloaded_file))
#
#             # Очищаем таблицу sapa и вставляем новые данные
#             db_connect.execute_set_sql_query("DELETE FROM sapa")
#             for _, row in df.iterrows():
#                 # Вставка данных в таблицу sapa
#                 insert_sapa_query = "INSERT INTO sapa (fullname, email, table_number, score) VALUES (%s, %s, %s, %s)"
#                 insert_params = (row['fullname'], row['email'], row['table_number'], row['score'])
#                 db_connect.execute_set_sql_query(insert_sapa_query, insert_params)
#
#                 # Обновляем или вставляем данные в sapa_bonus
#                 check_user_query = "SELECT bonus_score FROM sapa_bonus WHERE email = %s"
#                 result = db_connect.execute_get_sql_query(check_user_query, (row['email'],))
#
#                 if result:
#                     # Если пользователь уже существует, пересчитаем total_score
#                     current_bonus_score = result[0][0]  # Используем числовой индекс [0][0]
#                     new_total_score = current_bonus_score + row['score']
#                     update_total_score_query = """
#                         UPDATE sapa_bonus
#                         SET total_score = %s
#                         WHERE email = %s
#                     """
#                     db_connect.execute_set_sql_query(update_total_score_query, (new_total_score, row['email']))
#                 else:
#                     # Если пользователь не существует, добавим его с начальным значением bonus_score = 0
#                     insert_user_query = """
#                         INSERT INTO sapa_bonus (email, bonus_score, total_score)
#                         VALUES (%s, %s, %s)
#                     """
#                     insert_params = (row['email'], 0, row['score'])
#                     db_connect.execute_set_sql_query(insert_user_query, insert_params)
#
#             bot.send_message(user_id, "Таблица успешно обновлена!")
#             msg = bot.send_message(user_id, "Выберите один из доступных вариантов ниже:")
#             bot.register_next_step_handler(msg, sapa_instruments, bot)
#         except Exception as e:
#             bot.send_message(user_id, f"Ошибка при загрузке таблицы: {e}")
#     else:
#         bot.send_message(user_id, "Пожалуйста, загрузите файл в формате Excel.")
#         msg = bot.send_message(user_id, "Выберите один из доступных вариантов ниже:")
#         bot.register_next_step_handler(msg, sapa_instruments, bot)

def upload_sapa_table(message, bot):
    bot.send_message(message.chat.id, "Еще в разработке")
    bot.send_message(message.chat.id, "Пожалуйста вернитесь в главное меню. Написав команду '/menu'")
    # user_id = str(message.chat.id)
    # if message.content_type == 'document':
    #     file_info = bot.get_file(message.document.file_id)
    #     downloaded_file = bot.download_file(file_info.file_path)
    #
    #     try:
    #         # Загружаем данные из Excel файла в DataFrame
    #         df = pd.read_excel(io.BytesIO(downloaded_file))
    #
    #         # Очищаем таблицу sapa и вставляем новые данные
    #         db_connect.execute_set_sql_query("DELETE FROM sapa")
    #         for _, row in df.iterrows():
    #             # Вставка данных в таблицу sapa
    #             insert_sapa_query = "INSERT INTO sapa (fullname, email, table_number, score) VALUES (%s, %s, %s, %s)"
    #             insert_params = (row['fullname'], row['email'], row['table_number'], row['score'])
    #             db_connect.execute_set_sql_query(insert_sapa_query, insert_params)
    #
    #             # Обновляем или вставляем данные в sapa_bonus
    #             check_user_query = "SELECT bonus_score FROM sapa_bonus WHERE email = %s"
    #             result = db_connect.execute_get_sql_query(check_user_query, (row['email'],))
    #
    #             if result:
    #                 # Если пользователь уже существует, пересчитаем total_score
    #                 current_bonus_score = result[0][0]  # Используем числовой индекс [0][0]
    #                 new_total_score = current_bonus_score + row['score']
    #                 update_total_score_query = """
    #                     UPDATE sapa_bonus
    #                     SET total_score = %s
    #                     WHERE email = %s
    #                 """
    #                 db_connect.execute_set_sql_query(update_total_score_query, (new_total_score, row['email']))
    #             else:
    #                 # Если пользователь не существует, добавим его с начальным значением bonus_score = 0
    #                 insert_user_query = """
    #                     INSERT INTO sapa_bonus (email, bonus_score, total_score)
    #                     VALUES (%s, %s, %s)
    #                 """
    #                 insert_params = (row['email'], 0, row['score'])
    #                 db_connect.execute_set_sql_query(insert_user_query, insert_params)
    #
    #         bot.send_message(user_id, "Таблица успешно обновлена!")
    #         msg = bot.send_message(user_id, "Выберите один из доступных вариантов ниже:")
    #         bot.register_next_step_handler(msg, sapa_instruments, bot)
    #     except Exception as e:
    #         bot.send_message(user_id, f"Ошибка при загрузке таблицы: {e}")
    # else:
    #     bot.send_message(user_id, "Пожалуйста, загрузите файл в формате Excel.")
    #     msg = bot.send_message(user_id, "Выберите один из доступных вариантов ниже:")
    #     bot.register_next_step_handler(msg, sapa_instruments, bot)

def hse_competition_(bot, message, id_i_s = None):
    text = "Сохраненная информация\n\n"
    full_name = "ФИО: " + str(get_lastname(message)) + " " + get_firstname(message) + "\n"
    branch = "Дивизион: " + str(get_branch(message.chat.id)) + "\n"
    phone_num = "Номер телефона: " + str(get_phone_number(message)) + "\n"
    text = text + full_name + branch + phone_num + ("\n\nЕсли информация сохранена неправильно, "
                                                    "вы можете ее изменить нажав на /menu и перейти в Мой профиль")
    bot.send_message(message.chat.id, text)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup = generate_buttons(hse_com_field, markup)
    msg = bot.send_message(message.chat.id, "В каком конкурсе вы хотите принять участие?", reply_markup=markup)

    if redirect(bot, message, id_i_s):
        return
    else:
        bot.register_next_step_handler(msg, hse_get_competition_name, bot)


def hse_get_competition_name(message, bot, id_i_s=None):
    if redirect(bot, message, id_i_s):
        return
    else:
        hse_competition.insert_into_hse_competition(message.chat.id)
        hse_competition.set_competition(message.chat.id, message.text)
        msg = bot.send_message(message.chat.id, "Укажите свою должность")
        bot.register_next_step_handler(msg, hse_get_position, bot)


def hse_get_position(message, bot, id_i_s=None):
    if redirect(bot, message, id_i_s):
        return
    else:
        hse_competition.set_position(message.chat.id, message.text)
        msg = bot.send_message(message.chat.id, "С какого вы города?")
        bot.register_next_step_handler(msg, hse_get_city, bot)


def hse_get_city(message, bot, id_i_s=None):
    if redirect(bot, message, id_i_s):
        return
    else:
        user_id = message.chat.id
        # Обновляем город пользователя
        hse_competition.set_city(user_id, message.text)

        # Сохраняем текущее время
        current_time = datetime.now()  # Получаем текущее время
        hse_competition.set_time(user_id, current_time)  # Записываем время в базу

        bot.send_message(user_id,
                         "Поздравляю! Вы завершили регистрацию! \nВ ближайшее время с вами свяжутся наши организаторы")
        menu(bot, message)


def marathon(bot, message):
    bot.send_message(message.chat.id, "Для участия в цифровом марафоне, необходимо предоставить дополнительную "
                                      "информацию")
    if not maraphonersClass.ifExistsUser(message.chat.id):
        maraphonersClass.insert_into_maraphoners(message)
    msg = bot.send_message(message.chat.id, "Напишите вашу должность")
    bot.register_next_step_handler(msg, change_position, bot)


def change_position(message_, bot):
    if check_is_command(bot, message_, message_.text):
        return
    maraphonersClass.set_position(message_, message_.text)
    msg = bot.send_message(message_.chat.id, "Введите ваш возраст")
    bot.register_next_step_handler(msg, change_age, bot)


def change_age(message_, bot):
    if check_is_command(bot, message_, message_.text):
        return
    try:
        age = int(message_.text)
        if age < 5 or age > 100:
            raise ValueError("Возраст вне допустимого диапазона")
    except ValueError:
        msg = bot.send_message(message_.chat.id, "Введите ваш возраст")
        bot.register_next_step_handler(msg, change_age, bot)
        return
    maraphonersClass.set_age(message_, message_.text)
    markup_ = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup_ = generate_buttons(regions_, markup_)
    msg = bot.send_message(message_.chat.id, "Выберите ваш регион", reply_markup=markup_)
    bot.register_next_step_handler(msg, change_region, bot)


def change_region(message_, bot):
    if check_is_command(bot, message_, message_.text):
        return
    if message_.text not in regions_:
        markup_ = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_ = generate_buttons(regions_, markup_)
        msg = bot.send_message(message_.chat.id, "Необходимо выбрать ваш регион из списка", reply_markup=markup_)
        bot.register_next_step_handler(msg, change_region, bot)
        return
    maraphonersClass.set_region(message_, message_.text)
    formatted_number = str(maraphonersClass.get_id(message_)).zfill(4)

    bot.send_message(message_.chat.id,
                     "Регистрация закончена!\nВаш регистрационный номер\n<b>" + formatted_number + "</b>")
    bot.send_message(message_.chat.id, str(marathoner_text(message_.chat.id)) +
                     "\nЕсли данные указаны неверно, вернитесь в Главное меню /menu."
                     "\nДля исправления информации о должности, возрасте или регионе проживания пройдите регистрацию "
                     "на цифровой марафон снова."
                     "\n\nДля других данных нажмите кнопку '<b>Мой профиль</b>'")
    bot.send_message(message_.chat.id, "Пройдите по ссылке, чтобы попасть на официальный "
                                       "телеграм-канал марафона (вся информация будет высылаться туда). "
                                       "\nССЫЛКА: https://t.me/+edydGmWNMh43Zjcy")


# SELECT maraphoners.id, maraphoners.user_id, users.firstname, users.lastname, phone_number, branch, '
# age, position, region
def marathoner_text(user_id):
    marathoner_info = maraphonersClass.get_by_user_id(user_id)[0]
    text = f"ФИО: {marathoner_info[2]} {marathoner_info[3]}\n" \
           f"Номер телефона: {marathoner_info[4]}\n" \
           f"Филиал: {marathoner_info[5]}\n" \
           f"Должность: {marathoner_info[7]}\n" \
           f"Регион: {str(marathoner_info[8])}\n" \
           f"Возраст: {str(marathoner_info[6])}\n"
    return text


def start_adaption(bot, message):
    markup_adapt = types.InlineKeyboardMarkup()
    button_adapt = types.InlineKeyboardButton("Рассказывай!", callback_data="Рассказывай!")
    markup_adapt.add(button_adapt)
    bot.send_message(message.chat.id, f'Добро пожаловать в AO “Казахтелеком”🥳')
    send_photo_(bot, message.chat.id, 'images/dear_collegue.jpeg')
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Только для начала расскажу тебе, как мной пользоваться 🫡",
                     reply_markup=markup_adapt)


def adaption(bot, message):
    if message.text == "😊Welcome курс | Адаптация":
        if get_branch(message.chat.id) == "Дирекция Телеком Комплект":
            markup_dtk = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            button_dtk1 = types.KeyboardButton("Общая информация")
            button_dtk2 = types.KeyboardButton("ДТК")
            markup_dtk.add(button_dtk1, button_dtk2)
            bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_dtk)
        else:
            start_adaption(bot, message)
    elif message.text == "ДТК":
        markup_dtk = types.ReplyKeyboardMarkup(row_width=1)
        button_dtk1 = types.KeyboardButton("ДТК Инструкции")
        button_dtk2 = types.KeyboardButton("Приветствие")
        markup_dtk.add(button_dtk2, button_dtk1)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_dtk)
    elif message.text == "Общая информация":
        start_adaption(bot, message)
    elif message.text == "Приветствие":
        markup_adapt = types.InlineKeyboardMarkup()
        button_adapt = types.InlineKeyboardButton("Начинаем!", callback_data="Начинаем!")
        markup_adapt.add(button_adapt)
        bot.send_message(message.chat.id, '<b>Добро пожаловать на курс адаптации для филиала Дирекции '
                                          '«Телеком Комплект»!</b>'
                                          '\n\nМы рады приветствовать вас в нашей команде и уверены, что ваше '
                                          'сотрудничество с нами будет результативным и плодотворным.\nВ этом курсе вы '
                                          'ознакомитесь с нашей историей, корпоративной культурой, рабочими процессами '
                                          'и многим другим.')
        bot.send_photo(message.chat.id, photo=open('images/баннер - добро пожаловать - ДТК.png', 'rb'),
                       reply_markup=markup_adapt)
    else:
        instructions_dtk(bot, message)


def instructions_dtk(bot, message):
    message_text = message.text
    if message_text == "ДТК Инструкции":
        markup_dtk = types.ReplyKeyboardMarkup(row_width=1)
        button_dtk1 = types.KeyboardButton("Заявки в ОЦО HR")
        button_dtk2 = types.KeyboardButton("Заявки возложение обязанностей")
        button_dtk3 = types.KeyboardButton("Заявки на отпуск")
        button_dtk4 = types.KeyboardButton("Командировки")
        button_dtk5 = types.KeyboardButton("Переводы")
        button_dtk6 = types.KeyboardButton("Порядок оформления командировки")
        button_dtk7 = types.KeyboardButton("Рассторжение ТД")
        markup_dtk.add(button_dtk1, button_dtk2, button_dtk3, button_dtk4, button_dtk5, button_dtk6, button_dtk7)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_dtk)
    elif message_text == "Заявки в ОЦО HR":
        bot.send_document(message.chat.id, open("files/dtk/Заявки в ОЦО HR.docx", 'rb'))
        bot.send_document(message.chat.id, open("files/dtk/Заявки в ОЦО HR.pdf", 'rb'))
    elif message_text == "Заявки возложение обязанностей":
        bot.send_document(message.chat.id, open("files/dtk/заявки возложение обязанностей.docx", 'rb'))
        bot.send_document(message.chat.id, open("files/dtk/заявки возложение обязанностей.pdf", 'rb'))
    elif message_text == "Заявки на отпуск":
        bot.send_document(message.chat.id, open("files/dtk/заявки на отпуск.docx", 'rb'))
        bot.send_document(message.chat.id, open("files/dtk/заявки на отпуск.pdf", 'rb'))
    elif message_text == "Командировки":
        bot.send_document(message.chat.id, open("files/dtk/Авансовый отчет.pptx", 'rb'))
        bot.send_document(message.chat.id, open("files/dtk/командировка.pptx", 'rb'))
    elif message_text == "Переводы":
        bot.send_document(message.chat.id, open("files/dtk/Переводы.docx", 'rb'))
        bot.send_document(message.chat.id, open("files/dtk/Переводы.pdf", 'rb'))
    elif message_text == "Порядок оформления командировки":
        bot.send_document(message.chat.id, open("files/dtk/Порядок оформления командировки.docx", 'rb'))
        bot.send_document(message.chat.id, open("files/dtk/Порядок оформления командировки.pdf", 'rb'))
    elif message_text == "Рассторжение ТД":
        bot.send_document(message.chat.id, open("files/dtk/Рассторжение ТД.docx", 'rb'))
        bot.send_document(message.chat.id, open("files/dtk/Рассторжение ТД.pdf", 'rb'))


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

def call_back(bot, call):
    user_id = call.from_user.id
    response = call.data  # Assuming the response comes through call.data

    if str(user_id) in sapa_admin and response.startswith(('пост', 'пост1', 'отзыв', 'ничего')):
        try:
            parts = response.split(' ')
            if len(parts) == 2 and parts[1].isdigit():
                link_type = parts[0].lower()
                link_id = parts[1]

                # Удаление кнопок после выбора
                try:
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
                except Exception as e:
                    bot.send_message(call.message.chat.id, f"Ошибка при удалении кнопок: {e}")

                bonus_points = {
                    "пост": 500,
                    "пост1": 1000,
                    "отзыв": 1000,
                    "ничего": 0
                }
                new_bonus_score = bonus_points.get(link_type, 0)

                # Retrieve email and link
                link_result = db_connect.execute_get_sql_query(
                    "SELECT email, link FROM sapa_link WHERE id = %s", (link_id,)
                )
                if link_result:
                    email, link = link_result[0]

                    if email:
                        email = email.strip()
                    else:
                        email = get_user_email(user_id)

                    # Update link status
                    db_connect.execute_set_sql_query("""
                        UPDATE sapa_link 
                        SET is_checked = TRUE, status = %s 
                        WHERE id = %s
                    """, (link_type, link_id))

                    # Award points to the user
                    db_connect.execute_set_sql_query("""
                        UPDATE sapa_bonus 
                        SET bonus_score = bonus_score + %s, total_score = total_score + %s 
                        WHERE email = %s
                    """, (new_bonus_score, new_bonus_score, email))

                    bot.send_message(call.message.chat.id,
                                     f"Ссылка одобрена. Участнику начислено {new_bonus_score} баллов за тип '{link_type}'!")

                    user_result = db_connect.execute_get_sql_query(
                        "SELECT id FROM users WHERE email = %s", (email,)
                    )

                    if user_result:
                        user_chat_id = user_result[0][0]

                        # Extract bonus and total score for the user
                        score_result = db_connect.execute_get_sql_query(
                            """
                            SELECT sb.bonus_score, sb.total_score 
                            FROM sapa_bonus sb
                            JOIN sapa_link sl ON sb.email = sl.email
                            WHERE sl.id = %s
                            """,
                            (link_id,)
                        )

                        if score_result:
                            bonus_score = new_bonus_score
                            total_score = score_result[0][1]

                            message = (
                                f"Ваша ссылка была проверена.\n"
                                f"Бонусные баллы за эту ссылку: {bonus_score}\n"
                                f"Общий счёт: {total_score}"
                            )
                            bot.send_message(user_chat_id, message)
                            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                            markup.add(
                                # types.KeyboardButton('бонусная система SAPA+'),
                                       types.KeyboardButton('Инструкции, техническая поддержка и точки передачи'))

                            msg = bot.send_message(user_id, "Выберите одно из действий:", reply_markup=markup)
                            bot.register_next_step_handler(msg, sapa_con, bot)
                        else:
                            bot.send_message(user_chat_id, "Бонусные баллы и общий счёт не найдены.")
                            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                            markup.add(
                                # types.KeyboardButton('бонусная система SAPA+'),
                                       types.KeyboardButton('Инструкции, техническая поддержка и точки передачи'))

                            msg = bot.send_message(user_id, "Выберите одно из действий:", reply_markup=markup)
                            bot.register_next_step_handler(msg, sapa_con, bot)
                    else:
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        markup.add(
                            # types.KeyboardButton('бонусная система SAPA+'),
                                   types.KeyboardButton('Инструкции, техническая поддержка и точки передачи'))

                        msg = bot.send_message(user_id, "Выберите одно из действий:", reply_markup=markup)
                        bot.register_next_step_handler(msg, sapa_con, bot)
                else:
                    bot.send_message(call.message.chat.id, "Ошибка: ссылка не найдена.")
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                    markup.add(
                        # types.KeyboardButton('бонусная система SAPA+'),
                               types.KeyboardButton('Инструкции, техническая поддержка и точки передачи'))

                    msg = bot.send_message(user_id, "Выберите одно из действий:", reply_markup=markup)
                    bot.register_next_step_handler(msg, sapa_con, bot)
            else:
                bot.send_message(call.message.chat.id,
                                 "Некорректный ответ. Пожалуйста, выберите тип ссылки и укажите номер ссылки.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Ошибка при обработке ответа администратора: {e}")


    elif call.data == 'Начинаем!':
        cm_sv_db(call.message, 'Начинаем!')
        time.sleep(0.75)
        bold_text = ("В этом разделе вы ознакомитесь с организационной структурой Дирекции «Телеком Комплект», что "
                     "поможет вам лучше понять, как функционирует наша дирекция и какие подразделения в нее входят.")
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="ДалееИстория")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, bold_text, parse_mode='HTML')
        bot.send_photo(call.message.chat.id, photo=open('images/Орг.структура ДТК.jpg', 'rb'),
                       reply_markup=markup_callback)
    elif call.data == 'ДалееИстория':
        bot.send_message(call.message.chat.id, 'Здесь вы сможете ознакомиться с увлекательной историей филиала ДТК. '
                                               'Также узнайте больше о становлении, развитии и '
                                               'достижениях на этом пути.')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Продолжаем", callback_data="Продолжаем")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/баннер ИСТОРИЯ ДТК.png', 'rb'),
                       reply_markup=markup_callback)
    elif call.data == 'Продолжаем':
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="ДалееПроцессы")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, '<b>Централизованные процессы</b>\n\n'
                                               'В нашей компании централизованы следующие процессы: канцелярия, '
                                               'рекрутинг, кадровое делопроизводство, начисление заработной платы, '
                                               'закупочная система.\n\n'
                                               'В этом разделе вы можете подать заявку по кадровым вопросам:\n'
                                               'Перевод\n'
                                               'Отпуск\n'
                                               'Командировка\n'
                                               'Расторжение трудового договора\n'
                                               'Заявка на справку с места работы\n\n'
                                               'Все документы вы можете найти в разделе "ДТК Инструкции"',
                         reply_markup=markup_callback)
    elif call.data == 'ДалееПроцессы':
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="ДалееДосуг")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, 'В ДТК есть своя футбольная команда, неоднократный победитель турниров '
                                               'по футболу среди команд филиалов, компаний фонда «Самрук-Казына». ')
        bot.send_photo(call.message.chat.id, open('images/футбольная команда.jpeg', 'rb'))
        bot.send_photo(call.message.chat.id, open('images/футбольная команда1.jpeg', 'rb'))
        bot.send_message(call.message.chat.id, 'Также наши сотрудники активно участвуют в теннисных турнирах.\n'
                                               'В июне 2023 года мы провели мероприятие, посвященное 25-летию ДТК.',
                         reply_markup=markup_callback)
    elif call.data == 'ДалееДосуг':
        bot.send_message(call.message.chat.id, '<b>Дополнительные ресурсы</b>')
        bot.send_message(call.message.chat.id, '<b>Ссылки на социальные сети:</b>\n'
                                               '📰Telegram ДТК новости: https://t.me/+4bTQUYHNwdY4NDk6\n'
                                               '🗣Телеграмм ДТК cұхбат: https://t.me/+cgmlfGmotxM2NzZi\n'
                                               '📘Facebook: https://www.facebook.com/profile.php?'
                                               'id=100080229919711&mibextid=LQQJ4d')
        bot.send_message(call.message.chat.id, '<b>Ссылки на веб-ресурсы:</b>\n'
                                               '📊Система сбалансированных показателей '
                                               'http://bsc.telecom.kz/site/login\n'
                                               '🌐Эко система АО «Казахтелеком» '
                                               'https://portal.telecom.kz/')
        bot.send_message(call.message.chat.id, "Чтобы перейти в главное меню, введите или нажмите на команду \n/menu")
    elif call.data == 'Рассказывай!':
        cm_sv_db(call.message, 'Рассказывай!')
        send_photo_(bot, call.message.chat.id, 'images/picture.jpg')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Понятно", callback_data="Понятно")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "У меня есть клавиатура⌨️, пользуясь которой ты можешь переходить по "
                                               "разделам и получать нужную для тебя информацию",
                         reply_markup=markup_callback)
    elif call.data == "Понятно":
        send_photo_(bot, call.message.chat.id, 'images/hello.jpg')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Поехали!", callback_data="Поехали!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Жми на кнопку ниже👇🏻 и мы продолжаем.", reply_markup=markup_callback)
    elif call.data == "Поехали!":
        bot.send_photo(call.message.chat.id, photo=open('images/kaztelecom_credo.jpeg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "AO 'Казахтелеком' - это крупнейшая телекоммуникационная компания "
                                               "Казахстана,  образованная в соответствии c постановлением Кабинета "
                                               "Министров Республики\\Казахстан от 17 июня 1994 года.\n\n📌У нас есть "
                                               "краткая история o компании, которую мы подготовили специально для тебя."
                                               "Просто открой файлы ниже и ознакомься c ней.")
        bot.send_document(call.message.chat.id, open('images/PDF-1.jpg', 'rb'))
        bot.send_document(call.message.chat.id, open('images/PDF-2.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Да, давай!", callback_data="Да, давай!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Если все понятно, то продолжаем?", reply_markup=markup_callback)
    elif call.data == "Да, давай!":
        bot.send_message(call.message.chat.id, "У тебя уже есть Бадди?😁")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Если еще нет, не расстраивайся, он найдет тебя в ближайшее время!")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Да, хочу узнать больше!", callback_data="Да, хочу узнать больше!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Ты спросишь, a кто это и для чего он мне нужен? Отвечаю)",
                         reply_markup=markup_callback)
    elif call.data == "Да, хочу узнать больше!":
        bot.send_photo(call.message.chat.id, photo=open('images/Buddy-1.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_photo(call.message.chat.id, photo=open('images/Buddy-2.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Так что, проверь свой корпоративный e-мэйл, возможно тебе уже пришло "
                                               "сообщение от Твоего Бадди c предложением встретиться, познакомиться и "
                                               "рассказать o программе адаптации в нашей Компании.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Принято!", callback_data="Принято!")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/Buddy-3.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Принято!":
        bot.send_message(call.message.chat.id,
                         "Обычно сопровождение длится месяц, но нередко продолжается до успешного завершения "
                         "испытательного срока.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Кстати, участником программы Бадди может стать сотрудник любого отдела, и это здорово - "
                         "расширяются горизонтальные и вертикальные связи.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Круто, продолжаем дальше!",
                                                     callback_data="Круто, продолжаем дальше!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id,
                         "Позже и Ты тоже можешь стать Бадди и помогать будущим новичкам адаптироваться! 😊",
                         reply_markup=markup_callback)
    elif call.data == "Круто, продолжаем дальше!":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-1")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/credo_1.jpeg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Далее-1":
        bot.send_message(call.message.chat.id, "Наша компания состоит из 9 филиалов "
                                               "аббревиатуры которых ты точно будешь слышать в работе каждый день.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Поэтому давай познакомимся co структурой компании.")
        time.sleep(0.75)
        bot.send_document(call.message.chat.id, open('images/struct.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "A на случай если ты столкнешься c незнакомыми для тебя"
                         " терминами или аббревиатурами, то мы подготовили для тебя глоссарий в базе знаний.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Базу знаний ты всегда можешь найти в главном меню.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-3")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/gloss.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Далее-3":
        bot.send_message(call.message.chat.id,
                         'B компании AO "Казахтелеком" есть продукты по разным направлениям:\
                         \n🌍Интepнeт\n📞Teлeфoния\n📹Bидeoнabлюдeниe\n🖥️TV+\n🛍️Maraзин shop.telecom.kz')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-4")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id,
                         "Актуальную информацию по продуктам и их тарифам ты всегда сможешь найти на сайте telecom.kz",
                         reply_markup=markup_callback)
    elif call.data == "Далее-4":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-5")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/dear_users.jpeg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Далее-5":
        bot.send_message(call.message.chat.id, "☎️B AO 'Казахтелеком' интегрирована горячая линия «Нысана», "
                                               "куда каждый работник сможет обратиться посредством QR-кода "
                                               "или по контактам ниже в картинке")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-6")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/call_center.jpeg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Далее-6":
        bot.send_message(call.message.chat.id, "Отлично! \nMы c тобой познакомились c основной информацией o компании.\
                                             \n\nTы всегда можешь воспользоваться базой знаний или разделом часто "
                                               "задаваемых вопросов в главном меню бота.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Понятно!", callback_data="Понятно!")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/picture.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Понятно!":
        cm_sv_db(call.message, 'Welcome курс | Адаптация end')
        bot.send_message(call.message.chat.id, "Поздравляю!\nTы прошел Welcome курс.\n\nДoбpo пожаловать в компанию!."
                                               "\nЗдесь вы найдете всю дополнительную информацию, "
                                               "необходимую для успешной работы.")
        bot.send_document(call.message.chat.id,
                          document=open("files/Приложение 2 Добро пожаловать в АО Казахтелеком.pptx", 'rb'))
        time.sleep(0.75)
        if get_branch(call.message.chat.id) == "Дирекция Телеком Комплект":
            markup_dtk = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            button_dtk = types.KeyboardButton("Welcome курс | Адаптация ДТК")
            markup_dtk.add(button_dtk)
            bot.send_message(call.message.chat.id, "Чтобы перейти в главное меню, введите или нажмите на команду "
                                                   "\n/menu "
                                                   "\n\n Или вы можете перейти в категорию "
                                                   "'Welcome курс | Адаптация ДТК'",
                             reply_markup=markup_dtk)
        bot.send_message(call.message.chat.id, "Чтобы перейти в главное меню, введите или нажмите на команду \n/menu")
    elif call.data == "checkPoint":
        markup_p = types.InlineKeyboardMarkup()
        button_p1 = types.InlineKeyboardButton("iOS", callback_data="iOS")
        button_p2 = types.InlineKeyboardButton("Android", callback_data="Android")
        markup_p.add(button_p1, button_p2)
        bot.send_message(str(call.message.chat.id), "Выберите категорию", reply_markup=markup_p)
    elif call.data == portal_[5]:
        markup_p = types.InlineKeyboardMarkup()
        button_p1 = types.InlineKeyboardButton(text="Ссылка на App Store",
                                               url="https://apps.apple.com/ru/app/check-point-capsule-connect/"
                                                   "id506669652")
        markup_p.add(button_p1)
        bot.send_message(str(call.message.chat.id),
                         "Ссылка на видео инструкцию checkpoint на iOS\nhttps://youtu.be/giK26_GgVgE ",
                         reply_markup=markup_p)
    elif call.data == portal_[6]:
        markup_p = types.InlineKeyboardMarkup()
        button_p2 = types.InlineKeyboardButton(text="Ссылка на PlayMarket",
                                               url="https://play.google.com/store/apps/details?id=com.checkpoint."
                                                   "VPN&hl=en&gl=US&pli=1")
        markup_p.add(button_p2)
        bot.send_message(str(call.message.chat.id),
                         "Ссылка на видео инструкцию checkpoint на Android\nhttps://youtu.be/KjL9tpunb4U",
                         reply_markup=markup_p)
    elif call.data == "abbr":
        msg = bot.send_message(call.message.chat.id, "Введите аббревиатуру")
        bot.register_next_step_handler(msg, get_abbr, bot)
    elif str(call.data).isdigit():
        appeal_id = str(call.data)
        appeal_info = get_appeal_by_id(appeal_id)[0]
        image_data = get_image_data(appeal_id)
        try:
            bot.send_photo(appeal_info[1], image_data)
        except:
            print("error")
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Написать исполнителю', callback_data=str(appeal_info[0]) + 'texting')
        text = performer_text(appeal_info)
        if appeal_info[12] != "" and appeal_info[12] is not None and appeal_info[12] != " ":
            if db_connect.get_sale(appeal_info[12])[10] == "Самостоятельно":
                button_ = types.InlineKeyboardButton("Добавить модем | симкарту",
                                                     callback_data=str(appeal_info[12]) + "add_modem")
                button_1 = types.InlineKeyboardButton("Добавить фотографию Акта",
                                                      callback_data=str(appeal_info[12]) + "add_act")
                markup.add(button_, button_1)
                bot.send_message(call.message.chat.id, text, reply_markup=markup)
                return
        markup.add(btn)
        bot.send_message(call.message.chat.id, text, reply_markup=markup)
    elif extract_number(call.data, r'^(\d+)texting') is not None:
        appeal_id = extract_number(call.data, r'^(\d+)texting')
        msg = bot.send_message(call.message.chat.id, 'Введите комментарий')
        bot.register_next_step_handler(msg, add_comment, bot, appeal_id, False)
    elif extract_text(call.data, r'^.*abbr_save$', 'abbr_save') is not None:
        text = extract_text(call.data, r'^.*abbr_save$', 'abbr_save')
        send_abbr(bot, call.message, text)
    elif extract_text(call.data, r'^.*abbr_add$', 'abbr_add') is not None:
        text = extract_text(call.data, r'^.*abbr_add$', 'abbr_add')
        msg = bot.send_message(call.message.chat.id, "Введите расшифровку аббревиатуры")
        bot.register_next_step_handler(msg, get_decoding, bot, text)
    elif extract_number(str(call.data), r'^(\d+)add_act') is not None:
        set_appeal_field(call.message, True)
        bot.send_message(call.message.chat.id, "Отправьте фотографию акта")
    elif extract_number(str(call.data), r'^(\d+)add_modem') is not None:
        lte_id = extract_number(str(call.data), r'^(\d+)add_modem')
        msg = bot.send_message(call.message.chat.id, "Введите серийный номер симкарты")
        bot.register_next_step_handler(msg, get_simcard, bot, lte_id)
    elif extract_number(str(call.data), r'^(\d+)statusinprocess') is not None \
            or extract_number(str(call.data), r'^(\d+)statusdecided$') is not None:
        appeal_id = extract_number(str(call.data), r'^(\d+)statusinprocess')
        if appeal_id is None:
            appeal_id = extract_number(str(call.data), r'^(\d+)statusdecided$')
            set_status(appeal_id, "Решено")
        else:
            set_status(appeal_id, "В процессе")
        now = datetime.now() + timedelta(hours=5)
        now_updated = remove_milliseconds(now)
        set_date_status(appeal_id, str(now_updated))
        bot.send_message(call.message.chat.id, "Статус изменен")
        admin_appeal_callback(call, bot, add_comment)
        appeal_info = get_appeal_by_id(appeal_id)[0]
        text = performer_text(appeal_info)
        bot.send_message(appeal_info[1], "Статус изменен")
        image_data = get_image_data(appeal_id)
        try:
            bot.send_photo(appeal_info[1], image_data)
        except:
            print("error")
        bot.send_message(appeal_info[1], text)
        if get_status(appeal_id)[0][0] == "Решено":
            appeal_ = get_appeal_by_id(appeal_id)
            if appeal_[0][3] in get_regions():
                bot.send_message(appeal_info[1], "Выша заявка принята. Спасибо большое за содейтвие")
                return
            markup_callback = types.InlineKeyboardMarkup(row_width=5)
            for i in range(1, 6):
                callback_d = str(i) + "evaluation" + str(appeal_info[0])
                button_callback = types.InlineKeyboardButton(i, callback_data=callback_d)
                markup_callback.add(button_callback)
            bot.send_message(appeal_info[1], "Оцените решенное обращение от 1 до 5\n\nГде 1 - очень плохо, "
                                             "5 - замечательно", reply_markup=markup_callback)
    elif extract_numbers_from_status_change_decided(str(call.data)) is not None:
        evaluation, appeal_id = extract_numbers_from_status_change_decided(str(call.data))
        set_evaluation(appeal_id, evaluation)
        bot.edit_message_text("Спасибо за Ваш отзыв\nВы помогаете нам стать лучше", call.message.chat.id,
                              call.message.message_id)
        bot.answer_callback_query(call.id)
    elif extract_number(str(call.data), r'^(\d+)lte') is not None:
        sale_id = extract_number(str(call.data), r'^(\d+)lte')
        appeal_id = db_connect.get_appeal_by_lte_id(sale_id)
        text = get_appeal_text_all(appeal_id)
        bot.send_message(call.message.chat.id, text)
    else:
        admin_appeal_callback(call, bot, add_comment)


def get_abbr(message, bot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Отправить аббревиатуру", callback_data=message.text + "abbr_save")
    button2 = types.InlineKeyboardButton("Добавить расшифровку", callback_data=message.text + "abbr_add")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите следующий шаг", reply_markup=markup)


def send_abbr(bot, message, text):
    bot.send_message(message.chat.id, "Аббревиатура сохранена, спасибо Вам за помощь")
    bot.send_message('6682886650', "Предложение добавления глоссария\n" + text)


def get_decoding(message, bot, text):
    send_abbr(bot, message, text + " - " + message.text)


def add_comment(message, bot, appeal_id, isAdmin=True):
    if isAdmin:
        comment_ = '\n' + "Исполнитель: "
    else:
        comment_ = '\n' + "Пользователь: "
    comment = str(get_comment(appeal_id)[0][0]) + comment_ + message.text
    set_comment(appeal_id, comment)
    appeal_info = get_appeal_by_id(appeal_id)[0]
    image_data = get_image_data(appeal_id)
    text = performer_text(appeal_info)
    performer_id = performerClass.get_performer_id_by_id(appeal_info[7])
    try:
        bot.send_photo(performer_id, image_data)
    except:
        print("error")
    if isAdmin:
        bot.send_message(appeal_info[1], text)
        bot.send_message(message.chat.id, "Комментарий добавлен")
    else:
        bot.send_message(performer_id, text)
        bot.send_message(message.chat.id, "Комментарий добавлен")


def appeal(bot, message, message_text):
    set_appeal_field(message, True)
    if message_text == "Мои обращения":
        markup_a = appeal_inline_markup(message)
        if markup_a.keyboard:
            bot.send_message(message.chat.id, "Здесь вы можете отслеживать статусы ваших обращений",
                             reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, "Тут пока пусто, "
                                              "\nно Вы можете оставить обращение и оно будет отображаться здесь")
    elif message_text == "Оставить обращение":
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button2_ap = types.KeyboardButton("Да")
        markup_ap.add(button2_ap)
        profile(bot, message)
        bot.send_message(message.chat.id, "Информация верна?", reply_markup=markup_ap)
    elif message_text == "Да":
        if get_category_users_info(message) == 'Портал "Бірлік"':
            appeal(bot, message, "portal")
            return
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_ap.add(types.KeyboardButton("Вопрос к EX"))
        markup_ap = generate_buttons(list(list_categories())[:4], markup_ap)
        markup_ap.add(types.KeyboardButton("Закупочная деятельность"))
        bot.send_message(message.chat.id, "Выберите категорию обращения", reply_markup=markup_ap)
    elif message_text == "portal":
        bot.send_message(message.chat.id, 'Пожалуйста, опишите ваше обращение:')
    elif message_text == "Закупочная деятельность":
        markup_a = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_a = generate_buttons(get_categories_by_parentcategory("Закупочная деятельность"), markup_a)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_a)
    elif message_text == "Вопрос к EX":
        branch = get_branch(message.chat.id)
        set_category(message, message_text)
        if branch == 'Обьединение Дивизион "Сеть"':
            markup_a = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup_a = generate_buttons(get_subsubcategories_by_subcategory('Обьединение Дивизион "Сеть"'), markup_a)
            bot.send_message(message.chat.id, "Выберите регион филиала", reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, опишите ваше обращение:')
    elif message_text in list_categories() or message_text in get_categories_by_parentcategory(
            "Закупочная деятельность"):
        set_category(message, message.text)
        bot.send_message(message.chat.id, 'Пожалуйста, опишите ваше обращение:')
    elif message_text == "Добавить фото":
        bot.send_message(message.chat.id, "Отправьте фотографию")
    elif message_text in get_subsubcategories_by_subcategory('Обьединение Дивизион "Сеть"'):
        set_subsubcategory_users_info(message.chat.id, message_text)
        bot.send_message(message.chat.id, 'Пожалуйста, опишите ваше обращение:')
    elif message.photo:
        file_info: object = bot.get_file(message.photo[-1].file_id)
        file_url = 'https://api.telegram.org/file/bot{}/{}'.format(db_connect.TOKEN, file_info.file_path)
        file = requests.get(file_url)
        appeal_id = db_connect.get_last_appeal(message.chat.id)[0][0]
        appeal_ = get_appeal_by_id(appeal_id)[0]
        performer_id = performerClass.get_performer_by_id(str(appeal_[7]))[0][1]
        set_image_data(appeal_id, file)
        image_data = get_image_data(appeal_id)
        if performer_id is None or performer_id == '' or len(str(performer_id)) == 0:
            end_appeal_gmail(bot, message, appeal_id, file_url)
        else:
            bot.send_photo(performer_id, image_data)
            end_appeal(bot, message, appeal_id)
    elif message_text == "Отправить без фото":
        appeal_id = db_connect.get_last_appeal(message.chat.id)[0][0]
        appeal_ = get_appeal_by_id(appeal_id)[0]
        performer_id = performerClass.get_performer_by_id(appeal_[7])[0][1]
        if performer_id is None or performer_id == '' or len(str(performer_id)) == 0:
            end_appeal_gmail(bot, message, appeal_id)
        else:
            end_appeal(bot, message, appeal_id)
    elif get_appeal_field(message) and get_category_users_info(message) != ' ':
        now = datetime.now() + timedelta(hours=5)
        now_updated = remove_milliseconds(now)
        category = get_category_users_info(message)
        branch = get_branch(message.chat.id)
        subsubcategory = None
        if category == "Вопрос к EX":
            if branch == 'Обьединение Дивизион "Сеть"':
                subsubcategory = str(get_subsubcategory_users_info(message.chat.id)).strip()
                performer_ = get_performer_by_subsubcategory(subsubcategory)
                performer_id = performer_[0][0]
            else:
                performer_id = get_performer_by_category_and_subcategory(category, branch)[0][0]
        else:
            performer_id = get_performer_id_by_category(category)

        if performer_id is None or performer_id == '' or len(str(performer_id)) == 0:
            add_appeal_gmail(message.chat.id, category, message.text, now_updated)
        else:
            add_appeal(message.chat.id, "Обращение принято", category, message.text, now_updated,
                       now_updated, performer_id, ' ', False, None, branch, subsubcategory)
        markup_ap = types.ReplyKeyboardMarkup()
        button1_ap = types.KeyboardButton("Добавить фото")
        button2_ap = types.KeyboardButton("Отправить без фото")
        markup_ap.add(button2_ap, button1_ap)
        bot.send_message(message.chat.id, "Хотели ли бы вы добавить фотографию к вашему обращению?",
                         reply_markup=markup_ap)
    else:
        admin_appeal(bot, message, message_text)


def end_appeal(bot, message, appeal_id):
    category = appealsClass.get_category_by_appeal_id(appeal_id)[0][0]
    subsubcategory = str(get_subsubcategory_users_info(message.chat.id)).strip()
    if subsubcategory is not None and len(str(subsubcategory)) != 0:
        performer_id = get_performer_by_subsubcategory(subsubcategory)[0][1]
    else:
        if category == "Вопрос к EX":
            subcategory = get_branch(message.chat.id)
            performer_id = get_performer_by_category_and_subcategory(category, subcategory)[0][1]
        else:
            performer_id = get_performer_by_category(category=category)[1]
    text = get_appeal_text_all(appeal_id)
    bot.send_message(performer_id, text)
    bot.send_message(message.chat.id, "Ваше обращения принято")
    clear_appeals(message)
    menu(bot, message)


def end_appeal_gmail(bot, message, appeal_id, file=None):
    appeal_ = get_appeal_by_id(appeal_id)[0]
    text = get_user_info(message.chat.id)
    appeal_text = f'{text} \n {get_appeal_text(appeal_id)}'
    send_gmails(appeal_text, appeal_[3], file)
    bot.send_message(str(message.chat.id), "Ваше обращение успешно отправлено")


def faq(bot, message):
    if message.text == "Часто задаваемые вопросы":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button_d = types.KeyboardButton("Демеу")
        button_hr = types.KeyboardButton("Вопросы к HR")
        button_1 = types.KeyboardButton("Вопросы по займам")
        button_p1 = types.KeyboardButton("Вопросы по закупочной деятельности")
        button_p2 = types.KeyboardButton("Вопросы по порталу закупок")
        markup_faq.add(button_d, button_hr, button_1, button_p1, button_p2)
        bot.send_message(message.chat.id, "Здесь Вы можете найти ответы на часто задаваемые вопросы",
                         reply_markup=markup_faq)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Ecли y Bac есть предложения/идеи по добавлению новых разделов или ответов "
                                          "на вопросы, то напишите нам на info.ktcu@telecom.kz - мы обязательно "
                                          "рассмотрим Ваше предложение и свяжемся c Вами.")
    elif message.text == "Демеу":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_1:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup=markup_faq)
    elif message.text == "Вопросы к HR":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_2:
            button_hr = types.KeyboardButton(key)
            markup_faq.add(button_hr)
        bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup=markup_faq)
    elif message.text == "Вопросы по займам":
        branch = get_branch(message.chat.id)
        if branch == "Центральный Аппарат":
            markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
            markup_faq = generate_buttons(branches[1:], markup_faq)
            bot.send_message(message.chat.id, "Выберите филиал", reply_markup=markup_faq)
        elif branch in branches[1:]:
            bot.send_message(message.chat.id, f"Филиал {branch}\n\n"
                                              "Все вопросы по займам Вы можете адресовать по следующим контактам:")
            func_branch(bot, message, branch)
    elif message.text == "Вопросы по закупочной деятельности":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_procurement_activities:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup=markup_faq)
    elif message.text == "Вопросы по порталу закупок":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_procurement_portal:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup=markup_faq)
    else:
        func_branch(bot, message, message.text)


def func_branch(bot, message, message_text):
    if message_text == "Корпоративный Университет":
        bot.send_message(message.chat.id, "Таспаева Гульшат Сериккалиевна\nФинансовый блок\nГлавный бухгалтер\n"
                                          "мобильный +7-701-780-64-34")
    elif message_text == "Дивизион Информационных Технологий":
        bot.send_message(message.chat.id, "Рысбеков Нуркен Алтынбаевич\nДепартамент финансового анализа и планирования"
                                          "\nВедущий экономист\nрабочий +7-727-398-91-53, мобильный +7-702-345-6292"
                                          "\n\nДусалиева Жанна Хабидуллаевна\nДепартамент финансового анализа и "
                                          "планирования\nВедущий специалист\nрабочий +7-727-398-91-49, "
                                          "мобильный +7-777-181-8919")
    elif message_text == "Дивизион по Корпоративному Бизнесу":
        bot.send_message(message.chat.id, "Уразбаев Ануар Талғатұлы\nФинансовый блок/Департамент экономики и финансов/"
                                          "Отдел бюджетирования и казначейства\nВедущий экономист\n"
                                          "рабочий +7-727-244-70-54 мобильный +7-747-106-37-63\n\n"
                                          "Зинелов Әділет Маратұлы\nФинансовый блок/Департамент экономики и финансов/"
                                          "Отдел бюджетирования и казначейства\nЭкономист\nрабочий +7-727-272-04-11 "
                                          "мобильный +7-707-315-55-59")
    elif message_text == "Дирекция Управления Проектами":
        bot.send_message(message.chat.id, "Шекенова Нургуль Жантасовна\nEX сектор\nEX operations\nрабочий "
                                          "+7-717-224-97-46 мобильный +7-747-403-82-92)")
    elif message_text == "Дирекция Телеком Комплект":
        bot.send_message(message.chat.id, "Рамазанқызы Айнұр\nОтдел экономики и финансов\nВедущий специалистn\n"
                                          "мобильный +7-777-241-2936")
    elif message_text == "Сервисная Фабрика":
        bot.send_message(message.chat.id, "Тезекбаев Максат Темирбековичn\nОтдел бюджетирования, экономики и финансов\n"
                                          "Ведущий экономист\nмобильный +7-708-694-75-40")
    elif message_text == "Дивизион по Розничному Бизнесу":
        markup_r = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_r = generate_buttons(drb_regions, markup_r)
        bot.send_message(message.chat.id, "Выберите регион", reply_markup=markup_r)
    elif message_text == 'Обьединение Дивизион "Сеть"':
        markup_r = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_r = generate_buttons(ods_regions, markup_r)
        bot.send_message(message.chat.id, "Выберите регион", reply_markup=markup_r)


def func_region(bot, message):
    if message.text == "Алматинский регион, г.Алматы":
        bot.send_message(message.chat.id, "Бекен Назгуль Нурмахановна\nДРБ/Отдел учета расходов\nВедущий специалист\n"
                                          "мобильный +7-707-701-6110")
    elif message.text == "Западный, Центральный регион":
        bot.send_message(message.chat.id,
                         "Жумабейсова Гульшара Касимкуловна\nДРБ/Отдел ввода оплаты\nВедущий специалист"
                         "\nрабочий +7-713-254-50-45, мобильный +7-775 751-1269")
    elif message.text == "Северный, Южный, Восточный регионы":
        bot.send_message(message.chat.id,
                         "Суханбердиева Малика Дауреновна\nДРБ/Отдел ввода оплаты\nВедущий специалист\n"
                         "мобильный +7-708-566-6834")
    elif message.text == "ДЭСД 'Алматытелеком'":
        bot.send_message(message.chat.id, "Мусрепбекова Маржан Жексенбайқызы\nФЭБ\nВедущий экономист\n+77021737933, "
                                          "+77272975716")
    elif message.text == "Южно-Казахстанский ДЭСД":
        bot.send_message(message.chat.id, "Есенбекова Сауле Рахимжановна\nФЭБ\nЛогистик\n+77017605836, +77252530225")
    elif message.text == "Кызылординский ДЭСД":
        bot.send_message(message.chat.id, "Уракбаева Акканыш Утегуловна\nФЭБ\nВедущий экономист\n+77002151447, "
                                          "+77242264333")
    elif message.text == "Костанайский ДЭСД":
        bot.send_message(message.chat.id, "Жунусова Динара Тимурхановна\nФЭБ\nЭкономист 1 категории\n+77052153323, "
                                          "+77142573004")
    elif message.text == "Восточно-Казахстанский ДЭСД":
        bot.send_message(message.chat.id, "Беркимбаев Жаслан Жакауович\nФЭБ\nВедущий экономист\n+77142393364, "
                                          "+77142573373")
    elif message.text == "Атырауский ДЭСД":
        bot.send_message(message.chat.id, "Кенжетаева Гульнара  Сагиндыковна\nФЭБ\nВедущий экономист\n+77017987499, "
                                          "+77172577588")
    elif message.text == "Актюбинский ДЭСД":
        bot.send_message(message.chat.id, "Дуйсенов Бауыржан Рысбаевич\nФЭБ\nВедущий логистик\n+77053444748, "
                                          "+77292301077")
    elif message.text == "ДЭСД 'Астана'":
        bot.send_message(message.chat.id, "Уатаева Камшат Мейрхановна\nФЭБ\nВедущий экономист\n+77779939323, "
                                          "+77232200318")
    elif message.text == "ТУСМ-1":
        bot.send_message(message.chat.id, "Кан Людмила Трофимовна\nТБ\nИнженер электросвязи 1 категории\n+77012262288, "
                                          "+77273844921")
    elif message.text == "ТУСМ-6":
        bot.send_message(message.chat.id, "Жук Светлана Ивановна\nТБ\nИнженер электросвязи 1 категории\n+77771517171, "
                                          "+77222642713")
    elif message.text == "ТУСМ-8":
        bot.send_message(message.chat.id, "Клюшина Ирина Александровна\nТБ\nИнженер электросвязи 1 категории\n"
                                          "+77771472072, +77143192751")
    elif message.text == "ТУСМ-10":
        bot.send_message(message.chat.id, "Кенжебаев Самат Оспанұлы\nТБ\nИнженер электросвязи 2 категории\n"
                                          "+77075652955, +77172594103")
    elif message.text == "ТУСМ-11":
        bot.send_message(message.chat.id, "Усенова Балжан Тузеловна\nТБ\nИнженер электросвязи 1 категории\n"
                                          "+77056846921, +77252449534")
    elif message.text == "ТУСМ-13":
        bot.send_message(message.chat.id, "Туржигитова Венера Амангельдиновна\nТБ\nТехник линейных сооружений связи и "
                                          "абонентских устройств 1 категории\n+77473021977, +77122366397")
    elif message.text == "ТУСМ-14":
        bot.send_message(message.chat.id, "Арыстанова Нургуль Аманжуловна\nТБ\nТехник линейных сооружений связи и "
                                          "абонентских устройств 1 категории\n+77711863815, +77132530638")
    elif message.text == "ГА":
        bot.send_message(message.chat.id, "Арефьева Марина Александровна\nФЭБ\nЭкономист 1 категории\n+77053882043, "
                                          "+77273312070")


def biot(bot, message):
    if message.text == "👷Заполнить карточку БиОТ":
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button = types.KeyboardButton("Опасный фактор/условие")
        button2 = types.KeyboardButton("Поведение при выполнении работ")
        button3 = types.KeyboardButton("Предложения/Идеи")
        markup.add(button, button2, button3)
        bot.send_message(message.chat.id,
                         "Вы заметили опасный фактор, небезопасное поведение или y Bac есть предложения/идеи по "
                         "улучшению безопасности и охраны труда на рабочем месте?",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Bыбepитe необходимую классификацию события и заполните карточку БиОТ.")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите "
                         "/menu в меню команд слева от строки ввода.")
    elif message.text == "Опасный фактор/условие":
        bot.send_message(message.chat.id,
                         "Если Вы заметили опасный фактор или условие в процессе работы, то перейдите по ссылке ниже "
                         "и заполните опросник: "
                         "\nhttps://docs.google.com/forms/d/1eizZuYiPEHYZ8A9-TQTvhQAHJHVtmJ0H90gxUsn5Ows/edit")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в "
                         "меню команд слева от строки ввода.")
    elif message.text == "Поведение при выполнении работ":
        bot.send_message(message.chat.id,
                         "Если Вы заметили риски в поведении при выполнении работ, то перейдите по ссылке ниже и "
                         "заполните опросник: \nhttps://docs.google.com/forms/d/e/1FAIpQLSftmGKV1hjBiMcwqKW1yIM83PIP"
                         "2eOPqU4afa8x9z3-VeHZKA/viewform?usp=sf_link")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от "
                         "строки ввода.")
    elif message.text == "Предложения/Идеи":
        bot.send_message(message.chat.id, "Если y Bac есть предложения или идеи, то перейдите по ссылке ниже и "
                                          "заполните опросник:\n"
                                          "https://docs.google.com/forms/d/e/1FAIpQLSdzvAVfVH2dhFyXceKTyhZhBx9TplXUp53"
                                          "uLTSNzw8FejpNoA/viewform")
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню "
                                          "команд слева от строки ввода.")


def instructions(bot, message):
    if message.text == "Логотипы и Брендбук":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("АО 'Казахтелеком'")
        button2_i = types.KeyboardButton("Корпоративный университет")
        markup_instr.add(button1_i, button2_i)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_instr)
    elif message.text == "Модемы | Настройка":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("ADSL модем")
        button2_i = types.KeyboardButton("IDTV приставки")
        button3_i = types.KeyboardButton("ONT модемы")
        button4_i = types.KeyboardButton("Router 4G and Router Ethernet")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_instr)
    elif message.text == "Lotus | Инструкции":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Данные по серверам филиалов")
        button2_i = types.KeyboardButton("Инструкция по установке Lotus")
        button3_i = types.KeyboardButton("Установочный файл Lotus")
        markup_instr.add(button1_i, button2_i, button3_i)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_instr)
    elif message.text == "CheckPoint VPN | Удаленная работа":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Инструкция по установке CheckPoint")
        button2_i = types.KeyboardButton("Установочный файл CheckPoint")
        markup_instr.add(button1_i, button2_i)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_instr)
    elif message.text == "Личный кабинет telecom.kz":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Как оплатить услугу")
        button2_i = types.KeyboardButton("Как посмотреть о деталях оплаты")
        button3_i = types.KeyboardButton("Как посмотреть подключенные услуги")
        button4_i = types.KeyboardButton("Раздел 'Мои Услуги'")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_instr)
    elif message.text == "Командировка | Порядок оформления":
        bot.send_document(message.chat.id, document=open("files/Порядок оформления командировки.pdf", 'rb'))
    elif message.text == "Данные по серверам филиалов":
        bot.send_document(message.chat.id, document=open("files/Данные по всем lotus серверам.xlsx", 'rb'))
    elif message.text == "Инструкция по установке Lotus":
        bot.send_document(message.chat.id, document=open("files/Инструкция по Lotus Notes на домашнем пк_.docx", 'rb'))
    elif message.text == "Установочный файл Lotus":
        bot.send_message(message.chat.id, "Установочный файл Lotus Notes: \nhttps://drive.google.com/drive/folders/"
                                          "1MrpjeXavmRnUMvYUiTcylhxAIEA6dvBb?usp=drive_link")
    elif message.text == "Инструкция по установке CheckPoint":
        bot.send_document(message.chat.id, document=open("files/Инструкция по установке CheckPoint.pdf", 'rb'))
    elif message.text == "Установочный файл CheckPoint":
        bot.send_document(message.chat.id, document=open("files/E85.40_CheckPointVPN.msi", 'rb'))
    elif message.text == "АО 'Казахтелеком'":
        bot.send_message(message.chat.id,
                         "Здесь Вы можете найти логотипы и брендбук АО 'Казахтелеком'\n"
                         "https://drive.google.com/drive/folders/1TJOkjRhZcNauln1EFqIN6sh_D78TXvF7?usp=drive_link")
    elif message.text == "Корпоративный университет":
        bot.send_message(message.chat.id,
                         "Здесь Вы можете найти логотипы и брендбук Каорпоративного университета\n"
                         "https://drive.google.com/drive/folders/10JQcSDebbsBFrVPjcxAlWGXLdbn937MX?usp=sharing")
    elif message.text == "Как оплатить услугу":
        bot.send_document(message.chat.id, document=open("files/Как оплатить услуги Казахтелеком.pdf", 'rb'))
    elif message.text == "Как посмотреть о деталях оплаты":
        bot.send_document(message.chat.id,
                          document=open("files/Как посмотреть информацию о деталях оплаты.pdf", 'rb'))
    elif message.text == "Как посмотреть подключенные услуги":
        bot.send_document(message.chat.id, document=open("files/Как посмотреть мои подключенные услуги.pdf", 'rb'))
    elif message.text == "Раздел 'Мои Услуги'":
        bot.send_document(message.chat.id, document=open("files/раздел «МОИ УСЛУГИ».pdf", 'rb'))
    elif message.text == "ADSL модем":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'ADSL модем' перейдите по ссылке"
                         "\nhttps://drive.google.com/drive/folders/1ZMcd4cVuX8_JUJ8OoN0rYx5d5DjwlEbz?usp=drive_link")
    elif message.text == "IDTV приставки":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'IDTV приставки' перейдите по ссылке"
                         "\nhttps://drive.google.com/drive/folders/1ZFbUrKi9QITBLkJQ93I45dxhINSsgv7H?usp=drive_link")
    elif message.text == "ONT модемы":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'ONT модемы' перейдите по ссылке"
                         "\nhttps://drive.google.com/drive/folders/1IiLJ14dKF3wQhoLYb18jJMLD6BNz3K7x?usp=drive_link")
    elif message.text == "Router 4G and Router Ethernet":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Router 4G and Router Ethernet' перейдите по ссылке"
                         "\nhttps://drive.google.com/drive/folders/1EkzERKwa-DTnMW86-qJGbc_YAU2k6A74?usp=drive_link")
    elif message.text == "Портал закупок | Инструкции":
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1_kb = types.KeyboardButton("Для инициаторов | Инструкции")
        button2_kb = types.KeyboardButton("Для секретарей | Инструкции")
        markup_kb.add(button1_kb, button2_kb)
        bot.send_message(message.chat.id, "Выберите инструкцию", reply_markup=markup_kb)
    elif message.text == "Для инициаторов | Инструкции":
        bot.send_message(message.chat.id, "https://youtu.be/RsNAa02QO0M")
        bot.send_document(message.chat.id, open("files/Инструкция по работе в системе Портал закупок 2.0.docx", "rb"))
    elif message.text == "Для секретарей | Инструкции":
        bot.send_message(message.chat.id, "Инструкции для секретарей"
                                          "\nhttps://disk.telecom.kz/index.php/s/kc8PfD44Qw6X8jM")
        bot.send_message(message.chat.id, "Пароль:\nsF21hOvUOp")
    elif message.text == "Улучшение Wi-Fi сигнала для абонентов":
        bot.send_message(message.chat.id, "Улучшение Wi Fi сигнала для абонентов  Важность и возможности - \n"
                                          "https://youtu.be/wZ9Nn6bQZs")
    elif message.text == "Настройка маршрутизатора и Mesh системы":
        bot.send_message(message.chat.id, "Видеоинструкция по настройкам маршрутизатора и Mesh системы - \n"
                                          "https://youtu.be/0ue5ODjIXXU")
    elif message.text == "Сеть и ТВ+":
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1_kb = types.KeyboardButton("Сетевая настройка и TCP/IP")
        button2_kb = types.KeyboardButton("Установка ТВ+ Казахтелеком")
        markup_kb.add(button1_kb, button2_kb)
        bot.send_message(message.chat.id, "Выберите инструкцию", reply_markup=markup_kb)
    elif message.text == "Сетевая настройка и TCP/IP":
        bot.send_document(message.chat.id, open("files/Инструкция по проверке состояния сетевой карты и настройка "
                                                "свойств протокола tcpipv4.pdf", "rb"))
    elif message.text == "Установка ТВ+ Казахтелеком":
        bot.send_document(message.chat.id,
                          open("files/Инструкция по установке приложения  «ТВ+ Казахтелеком ».pdf", "rb"))
    elif message.text == "Подключение телевизора в Wi-fi":
        bot.send_document(message.chat.id, open("files/Подключение телевизора к Wi-fi сети 5 Ггц.pdf", "rb"))
    elif message.text == 'Измерительные приборы':
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_kb = types.KeyboardButton("Измерительные приборы инструкция")
        button2_kb = types.KeyboardButton("Аннотация Инструкция для работы с измерительным прибором")
        markup_kb.add(button1_kb, button2_kb)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_kb)
    elif message.text == "Измерительные приборы инструкция":
        bot.send_document(message.chat.id, open("files/Измерительные приборы инструкция.pdf", "rb"))
    elif message.text == "Аннотация Инструкция для работы с измерительным прибором":
        bot.send_document(message.chat.id,
                          open("files/Аннотация Инструкция для работы с измерительным прибором.pdf", "rb"))
    elif message.text =="Инструкция для прохождения курсов ДО":
        bot.send_document(message.chat.id,
                          open("files/Инструкция для прохождения дистанционных курсов на портале LMS - 1.jpg", "rb"))


def kb(bot, message):
    if message.text == "🗃️База знаний":
        set_bool(message, False, False)
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_kb = types.KeyboardButton("База инструкций")
        button2_kb = types.KeyboardButton("Глоссарий")
        button3_kb = types.KeyboardButton("Полезные ссылки")
        button4_kb = types.KeyboardButton("Регламентирующие документы")
        markup_kb.add(button2_kb, button1_kb, button3_kb, button4_kb)
        bot.send_message(message.chat.id, "Добро пожаловать в мобильную базу знаний!", reply_markup=markup_kb)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Здесь вы найдете необходимые инструкции. Вы также можете воспользоваться поисковой системой, чтобы "
                         "найти глоссарий ключевых терминов, которые мы используем каждый день.")
    elif message.text == "База инструкций":
        set_bool(message, True, False)
        markup_instr = types.ReplyKeyboardMarkup(row_width=1)
        button1_kb = types.KeyboardButton("Логотипы и Брендбук")
        button2_kb = types.KeyboardButton("Личный кабинет telecom.kz")
        button3_kb = types.KeyboardButton("Модемы | Настройка")
        button4_kb = types.KeyboardButton("Lotus | Инструкции")
        button6_kb = types.KeyboardButton("CheckPoint VPN | Удаленная работа")
        button7_kb = types.KeyboardButton("Командировка | Порядок оформления")
        button8_kb = types.KeyboardButton("Портал закупок | Инструкции")
        button9_kb = types.KeyboardButton("Улучшение Wi-Fi сигнала для абонентов")
        button10_kb = types.KeyboardButton("Настройка маршрутизатора и Mesh системы")
        button11_kb = types.KeyboardButton("Сеть и ТВ+")
        button12_kb = types.KeyboardButton("ДТК Инструкции")
        button13_kb = types.KeyboardButton("Подключение телевизора в Wi-fi")
        button14_kb = types.KeyboardButton("Измерительные приборы")
        button15_kb = types.KeyboardButton("Инструкция для прохождения курсов ДО")
        markup_instr.add(button4_kb, button6_kb, button1_kb, button7_kb, button2_kb, button3_kb, button8_kb,
                         button9_kb, button10_kb, button11_kb, button14_kb, button12_kb, button13_kb, button15_kb)
        bot.send_message(message.chat.id, "Здесь Вы можете найти полезную для Bac инструкцию.",
                         reply_markup=markup_instr)
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Для выбора инструкции выберите категория, a затем саму инструкцию в меню-клавиатуре⌨️.")
    elif message.text == "ДТК Инструкции":
        instructions_dtk(bot, message)
    elif message.text == "Глоссарий":
        set_bool(message, False, True)
        bot.send_message(message.chat.id, "Глоссарий терминов и аббревиатур в компании AO Казахтелеком.")
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Для того, чтобы получить расшифровку аббревиатуры или описание термина- "
                                          "начните вводить слово и отправьте для получения информации.")
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Важно!\n\n- Вводите слово без ошибок и лишних символов.\n - Аббревиатуры важно вводить c "
                         "верхним регистром. Например: ЕППК, ОДС, ДИТ.")
    # elif message.text == "Сервис и Продажи":
    #     markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    #     button1_i = types.KeyboardButton("Личный кабинет telecom.kz")
    #     button2_i = types.KeyboardButton("Акции")
    #     button3_i = types.KeyboardButton("НРД")
    #     button4_i = types.KeyboardButton("Скрипты")
    #     button5_i = types.KeyboardButton("Тарифы")
    #     markup_instr.add(button1_i, button2_i, button3_i, button4_i, button5_i)
    #     bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_instr)
    elif message.text == "Полезные ссылки":
        set_bool(message, False, False)
        time.sleep(0.5)
        markup = useful_links()
        bot.send_message(message.chat.id, "Полезные ссылки", reply_markup=markup)
    elif message.text == "Регламентирующие документы":
        markup = types.InlineKeyboardMarkup()

        # Добавляем кнопки для документов, каждая на отдельной строке
        button1 = types.InlineKeyboardButton("Регламент взаимодействия", callback_data="doc1")
        button2 = types.InlineKeyboardButton("Порядок осуществления закупок", callback_data="doc2")
        button3 = types.InlineKeyboardButton("Политика УР от 21.04.2023", callback_data="doc3")
        button4 = types.InlineKeyboardButton("Политика в области энергоменеджмента", callback_data="doc4")
        button5 = types.InlineKeyboardButton("Политика в области обеспечения БиОТ", callback_data="doc5")

        # Размещаем каждую кнопку в отдельную строку
        markup.row(button1)
        markup.row(button2)
        markup.row(button3)
        markup.row(button4)
        markup.row(button5)

        # Отправляем сообщение с инлайн-кнопками
        bot.send_message(message.chat.id, "Выберите регламентирующий документ:", reply_markup=markup)


# def kb_service(bot, message):
#     if message.text == "Личный кабинет telecom.kz":
#         markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_i = types.KeyboardButton("Как оплатить услугу")
#         button2_i = types.KeyboardButton("Как посмотреть о деталях оплаты")
#         button3_i = types.KeyboardButton("Как посмотреть подключенные услуги")
#         button4_i = types.KeyboardButton("Раздел 'Мои Услуги'")
#         markup_instr.add(button1_i, button2_i, button3_i, button4_i)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_instr)
#     elif message.text == "Акции":
#         bot.send_document(message.chat.id, open("files/Скрипт по акции Почувствуй разницу!.docx", 'rb'))
#     elif message.text == "Скрипты":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("НЛТ-2022")
#         button2_s = types.KeyboardButton("Текст SMS уведомления")
#         button3_s = types.KeyboardButton("Повышение Тарифов, Скрипт")
#         button4_s = types.KeyboardButton("Скрипт замена оборудования")
#         button5_s = types.KeyboardButton("Скрипт замена оборудования ПСС, УП")
#         button6_s = types.KeyboardButton("Скрипт с КАТВ на ТВ+")
#         markup_s.add(button1_s, button2_s, button3_s, button4_s, button5_s, button6_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "НЛТ-2022":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("2022 НЛТ_Bereket A для ЦРК")
#         button2_s = types.KeyboardButton("2022 НЛТ_Bereket А для ЦАП")
#         button3_s = types.KeyboardButton("2022 НЛТ_Керемет TV для ЦАП")
#         button4_s = types.KeyboardButton("2022 НЛТ_Керемет TV для ЦРК")
#         button5_s = types.KeyboardButton("2022 НЛТ_Керемет Моbile для ЦАП")
#         button6_s = types.KeyboardButton("2022 НЛТ_Керемет Моbile для ЦРК")
#         markup_s.add(button1_s, button2_s, button3_s, button4_s, button5_s, button6_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Тарифы":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Save Desk - Тарифы для удержания")
#         button2_s = types.KeyboardButton("Раздаточный материал, Приказ 210")
#         button3_s = types.KeyboardButton("Действующие пакеты 2022")
#         button4_s = types.KeyboardButton("Дополнительные виды услуг и сервисов")
#         button5_s = types.KeyboardButton("Тарифы на организацию доступа к услугам")
#         button6_s = types.KeyboardButton("Тарифы на Интернет")
#         button7_s = types.KeyboardButton("Тарифы на услуги мобильной связи")
#         markup_s.add(button1_s, button2_s, button3_s, button4_s, button5_s, button6_s, button7_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "НРД":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Стандарты СО")
#         button2_s = types.KeyboardButton("Публичный договор")
#         button3_s = types.KeyboardButton("Правила класификации лицевых счетов")
#         markup_s.add(button1_s, button2_s, button3_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Save Desk - Тарифы для удержания":
#         bot.send_document(message.chat.id, open("files/Save Desk-Тарифы для удержания.pdf", 'rb'))
#     elif message.text == "Раздаточный материал, Приказ 210":
#         bot.send_document(message.chat.id,
#                           open("files/Раздаточный материал, с 01.08.2023, Приказ 210 от 28.07.2023.xlsx", 'rb'))
#     elif message.text == "Действующие пакеты 2022":
#         bot.send_document(message.chat.id, open("files/Каз-12 Действующие пакеты 2022.pdf", 'rb'))
#     elif message.text == "Дополнительные виды услуг и сервисов":
#         bot.send_document(message.chat.id, open("files/Каз-8-Дополнительные виды услуг и сервисов.pdf", 'rb'))
#     elif message.text == "Тарифы на организацию доступа к услугам":
#         bot.send_document(message.chat.id, open("files/Каз-4-Тарифы на организацию доступа к услугам.pdf", 'rb'))
#     elif message.text == "Тарифы на Интернет":
#         bot.send_document(message.chat.id, open("files/Каз 7-Тарифы на Интернет.pdf", 'rb'))
#     elif message.text == "Тарифы на услуги мобильной связи":
#         bot.send_document(message.chat.id, open("files/Каз 3-Тарифы на услуги мобильной связи.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Bereket A для ЦРК":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Bereket A для ЦРК.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Bereket А для ЦАП":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Bereket А для ЦАП.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Керемет TV для ЦАП":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Керемет TV для ЦАП.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Керемет TV для ЦРК":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Керемет TV  для ЦРК.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Керемет Моbile для ЦАП":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Керемет Моbile для ЦАП.pdf", 'rb'))
#     elif message.text == "2022 НЛТ_Керемет Моbile для ЦРК":
#         bot.send_document(message.chat.id, open("files/2022 НЛТ_Керемет Моbile  для ЦРК.pdf", 'rb'))
#     elif message.text == "Текст SMS уведомления":
#         bot.send_document(message.chat.id, open("files/Текст SMS увед, каз и рус.pdf", 'rb'))
#     elif message.text == "Повышение Тарифов, Скрипт":
#         bot.send_document(message.chat.id, open("files/Повышение тарифов, Скрипт - с 1 августа 2023.pdf", 'rb'))
#     elif message.text == "Скрипт замена оборудования":
#         bot.send_document(message.chat.id, open("files/П_Скрипт замена оборудования.pdf", 'rb'))
#     elif message.text == "Скрипт замена оборудования ПСС, УП":
#         bot.send_document(message.chat.id, open("files/П_Скрипт замена оборудования ПСС, УП.pdf", 'rb'))
#     elif message.text == "Скрипт с КАТВ на ТВ+":
#         bot.send_document(message.chat.id, open("files/К_Скрипт с КАТВ на ТВ+.pdf", 'rb'))
#     elif message.text == "Стандарты СО":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Внутренний клиент, Стандарты СО")
#         button2_s = types.KeyboardButton("Внешний клиент, Стандарты СО")
#         markup_s.add(button1_s, button2_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Внутренний клиент, Стандарты СО":
#         bot.send_document(message.chat.id, open("files/Внутренний клиент, Стандарты СО.pdf", 'rb'))
#     elif message.text == "Внешний клиент, Стандарты СО":
#         bot.send_document(message.chat.id, open("files/Внешний клиент, Стандарты СО.pdf", 'rb'))
#     elif message.text == "Публичный договор":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Публичный договор рус")
#         button2_s = types.KeyboardButton("Публичный договор каз")
#         markup_s.add(button1_s, button2_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Публичный договор рус":
#         bot.send_document(message.chat.id, open("files/Публичный договор рус.pdf", 'rb'))
#     elif message.text == "Публичный договор каз":
#         bot.send_document(message.chat.id, open("files/Публичный договор каз.pdf", 'rb'))
#     elif message.text == "Правила классификации лицевых счетов рус":
#         markup_s = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
#         button1_s = types.KeyboardButton("Публичный договор рус")
#         button2_s = types.KeyboardButton("Публичный договор каз")
#         markup_s.add(button1_s, button2_s)
#         bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_s)
#     elif message.text == "Правила классификации лицевых счетов рус":
#         bot.send_document(message.chat.id, open("files/Правила классификации лицевых счетов рус.pdf", 'rb'))
#     elif message.text == "Правила классификации лицевых счетов каз":
#         bot.send_document(message.chat.id, open("files/Правила классификации лицевых счетов каз.pdf", 'rb'))
#     elif message.text == "Как оплатить услугу":
#         bot.send_document(message.chat.id, document=open("files/Как оплатить услуги Казахтелеком.pdf", 'rb'))
#     elif message.text == "Как посмотреть о деталях оплаты":
#         bot.send_document(message.chat.id,
#                           document=open("files/Как посмотреть информацию о деталях оплаты.pdf", 'rb'))
#     elif message.text == "Как посмотреть подключенные услуги":
#         bot.send_document(message.chat.id, document=open("files/Как посмотреть мои подключенные услуги.pdf", 'rb'))
#     elif message.text == "Раздел 'Мои Услуги'":
#         bot.send_document(message.chat.id, document=open("files/РАЗДЕЛ «МОИ УСЛУГИ» (1).pdf", 'rb'))

def glossary(bot, message):
    text1 = f"По Вашему запросу нaйдeнo следующие значение:"
    text2 = ("Помогите нам стать лучше!\nЖдем вашего мнения и предложений.\n\n"
             "Вы можете отправить нам Вашу обратную связь нажав на кнопку 'написать сообщение' или отправив письмо на "
             "info.ktcu@telecom.kz.")
    button_text = "Написать аббревиатуру"
    common_file.glossary(bot, message, text1, text2, button_text)


def profile(bot, message):
    markup_ap = types.InlineKeyboardMarkup(row_width=1)
    button1_ap = types.InlineKeyboardButton("Изменить Имя", callback_data="Изменить Имя")
    button2_ap = types.InlineKeyboardButton("Изменить Фамилию", callback_data="Изменить Фамилию")
    button3_ap = types.InlineKeyboardButton("Изменить номер телефона", callback_data="Изменить номер телефона")
    button4_ap = types.InlineKeyboardButton("Изменить email", callback_data="Изменить email")
    button5_ap = types.InlineKeyboardButton("Изменить табельный номер", callback_data="Изменить табельный номер")
    button6_ap = types.InlineKeyboardButton("Изменить филиал", callback_data="Изменить филиал")
    markup_ap.add(button1_ap, button2_ap, button3_ap, button4_ap, button5_ap, button6_ap)
    user_info = get_user(message.chat.id)
    bot.send_message(message.chat.id, f"Сохраненная информация\n\n"
                                      f"Имя: {user_info[3]}\n"
                                      f"Фамилия: {user_info[2]}\n"
                                      f"Номер телефона: {user_info[5]}\n"
                                      f"Email: {user_info[6]}\n"
                                      f"Табельный номер: {user_info[4]}\n"
                                      f"Филиал: {user_info[7]}",
                     reply_markup=markup_ap)


def questions(bot, message):
    button_q = types.KeyboardButton("Мои обращения")
    button_q1 = types.KeyboardButton("Оставить обращение")
    button_q2 = types.KeyboardButton("Часто задаваемые вопросы")
    markup_q = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup_q.add(button_q2, button_q1, button_q)
    bot.send_message(str(message.chat.id), "B данном разделе Вы можете оставить свое обращение или "
                                           "посмотреть ответы на часто задаваемые вопросы", reply_markup=markup_q)
    time.sleep(0.75)
    bot.send_message(message.chat.id, "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu "
                                      "в меню команд слева от строки ввода.")


def portal(bot, message):
    message_text = message.text
    if message_text == '🖥Портал "Бірлік"':
        markup_p = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, )
        markup_p = generate_buttons(portal_bts, markup_p)
        bot.send_message(str(message.chat.id), "Выберите категорию", reply_markup=markup_p)
    elif message_text == portal_bts[0]:
        with open("images/Birlik_BG.jpg", 'rb') as photo_file:
            bot.send_photo(message.chat.id, photo_file)
        bot.send_message(str(message.chat.id), "Портал работника 'Бірлік' - единая интранет система, созданная в "
                                               "рамках фокусов цифровой трансформации для каждого работника АО "
                                               "'Казахтелеком'.\n"
                                               "Разделы которые есть и развиваются на портале:\n"
                                               "▪ Профиль\n"
                                               "▪ Новости\n"
                                               "▪ Сообщества\n"
                                               "▪ Календарь\n"
                                               "▪ Структура компании и карточка подразделений\n"
                                               "▪ Расширенный поиск\n"
                                               "▪ Афиша мероприятий\n"
                                               "▪ Интерактивная карта офиса\n"
                                               "▪ Опросы и тесты\n"
                                               "▪ Маркет и система геймификации\n\n"
                                               "Преимущества портала работника 'Бірлік':\n"
                                               "-     Единое информационное пространство\n"
                                               "Быстрый поиск нужной информации\n"
                                               "Эффективное сотрудничество и командная работа\n"
                                               "Укрепление корпоративной культуры и ценностей компании\n"
                                               "Интеграция внешних модулей в единое пространство")
    elif message_text == portal_[0]:
        markup_p = types.InlineKeyboardMarkup()
        button_p = types.InlineKeyboardButton("Нужен checkpoint?", callback_data="checkPoint")
        markup_p.add(button_p)
        bot.send_message(str(message.chat.id), "Как авторизоваться на портале работника на IOS и Android | "
                                               "portal.telecom.kz\nhttps://youtu.be/WJdS1aIBe1I", reply_markup=markup_p)
    # elif message_text == portal_bts[3]:
    #     markup_p = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, )
    #     markup_p = db_connect.generate_buttons(portal_guide, markup_p)
    #     bot.send_message(str(message.chat.id), "Выберите вопрос", reply_markup=markup_p)
    elif message_text == portal_bts[2]:
        set_category(message, 'Портал "Бірлік"')
        appeal(bot, message, message_text)
    else:
        if checkpoint(bot, message, message_text):
            return
        check_portal_guide(bot, message, message_text, portal_guide)


def checkpoint(bot, message, message_text):
    if message_text == portal_bts[1]:
        markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(portal_[0])
        button2 = types.KeyboardButton(portal_[1])
        markup_portal.add(button1, button2)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_portal)
    elif message_text == portal_[1]:
        markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_p = types.KeyboardButton("Как авторизоваться")
        button2_p = types.KeyboardButton("Личный профиль")
        button3_p = types.KeyboardButton("Из портала перейти в ССП")
        markup_pk.add(button1_p, button2_p, button3_p)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_pk)
    elif message_text == portal_[2]:
        bot.send_message(message.chat.id, "Для получения информации о категории 'Как авторизоваться на портале "
                                          "работника через ПК?' перейдите по ссылке ниже "
                                          "\nhttps://youtu.be/vsRIDqt_-1A")
    elif message_text == portal_[3]:
        bot.send_message(message.chat.id, "Для получения информации о категории 'Как заполнить личный профиль?' "
                                          "перейдите по ссылке ниже \nhttps://youtu.be/V9r3ALrIQ48")
    elif message_text == portal_[4]:
        bot.send_message(message.chat.id, "Для получения информации о категории 'Как перейти из портала перейти в ССП'"
                                          " перейдите по ссылке ниже \nhttps://youtu.be/wnfI4JpMvmE")
    else:
        return False
    return True


subscriber_types = ['Новый', 'Действующий']
lte_files = ["Инструкция 'Пилот LTE'", "Как подписать договор онлайн", "Скрипт на Алем",
             "Акт сдачи-приема выполненных работ", "Тарифы"]


def lte(message, bot, message_text=None):
    if message_text is None:
        message_text = message.text
    if message.text == lte_[0]:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_l = types.KeyboardButton(lte_[1])
        button2_l = types.KeyboardButton(lte_[2])
        button3_l = types.KeyboardButton(lte_[3])
        button4_l = types.KeyboardButton(lte_[4])
        markup_l.add(button1_l, button2_l, button3_l, button4_l)
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup_l)
    elif message.text == lte_[1]:
        bot.send_message(message.chat.id,
                         """
Представляем вам проект "Пилот LTE", нацеленный на укрепление нашей позиции на рынке и увеличение продаж в сегменте LTE. 

Наша цель
Достичь новых высот в продажах и увеличить нашу долю на растущем рынке LTE.

Длительность
до 31.12.2023 года.

Участники
 - по продаже услуг    и «LTE», проект открыт для всех сотрудников структурных подразделений Дивизиона по розничному бизнесу АО "Казахтелеком", исключая участников ЕМП.
  - по доставке клиентского оборудования, проект открыт для всех сотрудников структурных подразделений Дивизиона по розничному бизнесу АО "Казахтелеком", исключая участников ЕМП, кроме работников канала продаж «УП» и работников Отдела управления внешними каналами продаж

Преимущество участия в проекте заключается в том, что вы сможете увеличить свой доход, получая следующие бонусы:
 - 2500 тенге за успешную продажу услуги LTE.
 - 1591 тенге за доставку и настройку модема и сим-карты.
 - 
Присоединитесь к "Пилоту LTE" и помогите нам достичь новых успехов на рынке, а также увеличить вашу прибыль. 

Вместе мы сможем добиться больших результатов!""")
    elif message.text == lte_[2]:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(lte_files[0])
        button2 = types.KeyboardButton(lte_files[1])
        button3 = types.KeyboardButton(lte_files[2])
        button4 = types.KeyboardButton(lte_files[3])
        button5 = types.KeyboardButton(lte_files[4])
        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id, "Выберите файл", reply_markup=markup)
    elif message_text == lte_[3]:
        id_ = add_internal_sale(str(message.chat.id))
        markup_lte = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_lte = generate_buttons(subscriber_types, markup_lte)
        msg = bot.send_message(message.chat.id, "Выберите тип абонента", reply_markup=markup_lte)
        bot.register_next_step_handler(msg, add_subscriber, bot, id_)
    elif message_text == lte_[4]:
        markup_a = db_connect.my_lte(message.chat.id)
        if markup_a.keyboard:
            bot.send_message(message.chat.id, "Здесь вы можете отслеживать статусы ваших продаж",
                             reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, "Продаж не было")
    elif message_text == lte_files[0]:
        bot.send_document(message.chat.id, open('files/Инструкция Пилот LTE.pdf', 'rb'))
    elif message_text == lte_files[1]:
        bot.send_document(message.chat.id, open('files/Как подписать договор онлайн.pdf', 'rb'))
    elif message_text == lte_files[2]:
        bot.send_document(message.chat.id, open('files/Скрипт на Алем.docx', 'rb'))
        bot.send_document(message.chat.id, open('files/Скрипт на Алем.pdf', 'rb'))
    elif message_text == lte_files[3]:
        bot.send_document(message.chat.id, open('files/Акт сдачи-приема выполненных работ, '
                                                'оборудования и материалов.docx', 'rb'))
        bot.send_document(message.chat.id, open('files/Орындалған жұмыстарды, жабдықтар мен материалдарды қабылдау '
                                                'өткізу актісі.docx', 'rb'))
    elif message_text == lte_files[4]:
        bot.send_document(message.chat.id, open('files/Тарифы.pdf', 'rb'))


def add_subscriber(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in subscriber_types:
        markup_lte = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_lte = generate_buttons(subscriber_types, markup_lte)
        msg = bot.send_message(message.chat.id, "Выберите тип абонента из списка", reply_markup=markup_lte)
        bot.register_next_step_handler(msg, add_subscriber, bot, id_i_s)
        return
    set_subscriber_type(id_i_s, message.text)
    regions = get_regions()
    markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup_l = generate_buttons(regions, markup_l)
    msg = bot.send_message(message.chat.id, "Выберите регион", reply_markup=markup_l)
    bot.register_next_step_handler(msg, get_region, bot, id_i_s, regions)


def get_region(message, bot, id_i_s, regions):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in regions:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_l = generate_buttons(regions, markup_l)
        msg = bot.send_message(message.chat.id, "Выберите регион из списка", reply_markup=markup_l)
        bot.register_next_step_handler(msg, get_region, bot, id_i_s, regions)
        return
    performer_id = get_performer_by_category(message.text)[0]
    set_category_i_s(id_i_s, message.text)
    set_performer_id_i_s(id_i_s, performer_id)
    markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup_l.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
    msg = bot.send_message(message.chat.id,
                           "Абонент уведомлен о необходимости  предоставления следующих кодов/SMS работнику отдела CRM "
                           "и КС: \nкод для цифровых документов;\nSMS для верификации номера;\nкод для автоподписания "
                           "бланка заявления.", reply_markup=markup_l)
    bot.register_next_step_handler(msg, get_is_notified, bot, id_i_s)


def get_is_notified(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text != "Нет" and message.text != "Да":
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_l.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
        msg = bot.send_message(message.chat.id, "Выберите варианты из предложенного списка", reply_markup=markup_l)
        bot.register_next_step_handler(msg, get_is_notified, bot, id_i_s)
        return
    is_notified = True
    if message.text == "Нет":
        is_notified = False
    set_is_notified(id_i_s, is_notified)
    msg = bot.send_message(message.chat.id, "Введите ФИО абонента")
    bot.register_next_step_handler(msg, get_full_name, bot, id_i_s)


def get_full_name(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    set_full_name(id_i_s, message.text)
    msg = bot.send_message(message.chat.id, "Введите ИИН")
    bot.register_next_step_handler(msg, get_iin, bot, id_i_s)


def get_iin(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if not message.text.isdigit() or len(message.text) != 12:
        msg = bot.send_message(message.chat.id, "Введенная информация не соответствует шаблону ИИН, введите еще раз")
        bot.register_next_step_handler(msg, get_iin, bot, id_i_s)
        return
    set_iin(id_i_s, message.text)
    msg = bot.send_message(message.chat.id, "Введите номер телефона")
    bot.register_next_step_handler(msg, get_phone_num_i_s, bot, id_i_s)


def get_phone_num_i_s(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    pattern = r'^(\+?7|8)(\d{10})$'
    if not re.match(pattern, message.text):
        msg = bot.send_message(message.chat.id, "Введенная информация не соответствует шаблону 87001110000")
        bot.register_next_step_handler(msg, get_phone_num_i_s, bot, id_i_s)
        return
    set_phone_num_subscriber(id_i_s, message.text)
    msg = bot.send_message(message.chat.id, "Введите адрес абонента")
    bot.register_next_step_handler(msg, get_address_subscriber, bot, id_i_s)


def get_address_subscriber(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    set_subscriber_address(id_i_s, message.text)
    markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup_l = generate_buttons(pp, markup_l)
    msg = bot.send_message(message.chat.id, "Выберите ПП из списка", reply_markup=markup_l)
    bot.register_next_step_handler(msg, get_pp, bot, id_i_s)


delivery = ["Самостоятельно", "Силами другого подразделения"]
arr = ["Я продал!", "Я доставил!"]


def get_pp(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in pp:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_l = generate_buttons(pp, markup_l)
        msg = bot.send_message(message.chat.id, "Выберите ПП из списка", reply_markup=markup_l)
        bot.register_next_step_handler(msg,  get_pp, bot, id_i_s)
        return
    set_product_name(id_i_s, message.text)
    markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup_l = generate_buttons(arr, markup_l)
    msg = bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_l)
    bot.register_next_step_handler(msg, func_lte, bot, id_i_s)


def func_lte(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in arr:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_l = generate_buttons(arr, markup_l)
        msg = bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup_l)
        bot.register_next_step_handler(msg, func_lte, bot, id_i_s)
        return
    if message.text == arr[0]:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_l = generate_buttons(delivery, markup_l)
        set_action(id_i_s, "Продажа")
        msg = bot.send_message(message.chat.id, "Как будет осуществлена доставка?", reply_markup=markup_l)
        bot.register_next_step_handler(msg, get_delivery, bot, id_i_s)
    else:
        set_action(id_i_s, "Доставка")
        set_delivery(id_i_s, delivery[0])
        add_lte_appeal(bot, message, id_i_s)


def get_delivery(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    if message.text not in delivery:
        markup_l = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup_l = generate_buttons(delivery, markup_l)
        msg = bot.send_message(message.chat.id, "Как будет осуществлена доставка?", reply_markup=markup_l)
        bot.register_next_step_handler(msg, get_delivery, bot, id_i_s)
        return
    set_delivery(id_i_s, message.text)
    add_lte_appeal(bot, message, id_i_s)


def get_simcard(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    set_simcard(id_i_s, message.text)
    msg = bot.send_message(message.chat.id, "Введите серийный номер модема")
    bot.register_next_step_handler(msg, get_modem, bot, id_i_s)


def get_modem(message, bot, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    set_modem(id_i_s, message.text)
    appeal_ = db_connect.get_appeal_by_lte_id(id_i_s)
    simcard = lteClass.get_simcard(id_i_s)
    lte_info = db_connect.get_sale(id_i_s)
    is_notified = "Да"
    if not lte_info[7]:
        is_notified = "Нет"
    text = f"\n\tФИО абонента: {lte_info[3]}\n" \
           f"\tИИН: {lte_info[4]}\n" \
           f"\tНомер телефона абонента: {lte_info[5]}\n" \
           f"\tТип абонента: {lte_info[6]}\n" \
           f"\tУведомлен? {is_notified}\n" \
           f"\tАдрес абонента: {lte_info[8]}\n" \
           f"\tПП: {lte_info[9]}\n" \
           f"\tДоставка: {lte_info[10]}" \
           f"\n\tSimcard: {simcard}\n" \
           f"\tМодем: {message.text}"
    set_appeal_text(appeal_[0], text)
    bot.send_message(message.chat.id, "Информация сохранена")
    appeal_info = get_appeal_by_id(appeal_[0])[0]
    text = performer_text(appeal_info)
    performer_id = performerClass.get_performer_by_id(appeal_info[7])[0][1]
    bot.send_message(performer_id, "Информация по серийному номеру сим карты и модема добавлена")
    bot.send_message(performer_id, text)


def menu(bot, message):
    set_bool(message, False, False)
    markup = get_markup(message)
    bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=markup)


def add_lte_appeal(bot, message, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    lte_info = db_connect.get_sale(id_i_s)
    now = datetime.now() + timedelta(hours=5)
    now_updated = remove_milliseconds(now)
    is_notified = "Да"
    if not lte_info[7]:
        is_notified = "Нет"
    text = f"ФИО абонента: {lte_info[3]}\n" \
           f"\tИИН: {lte_info[4]}\n" \
           f"\tНомер телефона абонента: {lte_info[5]}\n" \
           f"\tТип абонента: {lte_info[6]}\n" \
           f"\tУведомлен? {is_notified}\n" \
           f"\tАдрес абонента: {lte_info[8]}\n" \
           f"\tПП: {lte_info[9]}\n" \
           f"\tДействие: {lte_info[14]}\n" \
           f"\tДоставка: {lte_info[10]}"
    if lte_info[10] == "Самостоятельно":
        text += f"\n\tSimcard: {is_none(lte_info[11])}\n" \
                f"\tМодем: {is_none(lte_info[12])}"

    appeal_id = add_appeal(message.chat.id, 'Обращение принято', lte_info[13], text, now_updated,
                           now_updated,
                           lte_info[2], ' ', False, id_i_s)
    text = get_appeal_text_all(appeal_id)
    performer_id = performerClass.get_performer_by_id(lte_info[2])[0][1]
    bot.send_message(performer_id, text)
    bot.send_message(message.chat.id, "Ваша информация сохранена")


def send_verification_code(user_id, bot, message):
    # Генерируем и сохраняем код подтверждения
    verification_code = generate_and_save_code(user_id)
    # Текст сообщения
    text = f"Ваш код подтверждения: {verification_code}"
    # Отправляем письмо через уже существующую функцию send_gmails
    common_file.send_gmails_for_verif(text, user_id, None)

    # Запускаем таймер на 5 минут
    start_verification_timer(user_id, bot, message)


# Словарь для хранения последних сообщений пользователей
user_message_history = {}


# Функция для добавления сообщения в историю пользователя
def add_message_to_history(user_id, message_text):
    # Получаем историю пользователя или создаем новую, если ее нет
    user_message_history[user_id] = user_message_history.get(user_id, [])

    # Ограничиваем количество сохраненных сообщений до 4
    if len(user_message_history[user_id]) >= 4:
        user_message_history[user_id].pop(0)  # Удаляем самое старое сообщение

    # Добавляем новое сообщение
    user_message_history[user_id].append(message_text)


def clear_message_history(user_id):
    if user_id in user_message_history:
        del user_message_history[user_id]

# Модифицированная функция для обработки верификации
def verify_code(message, bot):
    user_id = str(message.chat.id)

    # Проверка на наличие таймера в словаре
    if user_id not in verification_timers:
        return

    # Получаем введенный код и очищаем его от пробелов
    entered_code = message.text.strip()

    # Действия, если введена команда, начинающаяся с "/"
    if entered_code.startswith('/'):
        # Удаляем таймер, если он есть
        verification_timers.pop(user_id, None)
        # Переход в меню, если команда "/menu"
        if entered_code == '/menu':
            menu(bot, message)
            return True

    # Получение сохраненного кода
    saved_code = str(get_saved_verification_code(user_id)).strip()

    # Попытка преобразовать коды в числа и сравнить их
    try:
        entered_code = int(entered_code)
        saved_code = int(saved_code)

        # Проверка соответствия введенного и сохраненного кода
        if entered_code == saved_code:
            verification_timers.pop(user_id, None)  # Удаляем таймер
            # Обновляем статус пользователя в базе данных
            sql_query = "UPDATE users SET is_verified = TRUE WHERE id = %s"
            params = (user_id,)
            db_connect.execute_set_sql_query(sql_query, params)

            # Проверяем, есть ли в последних сообщениях "Регистрация на обучение"
            if check_registration_message_in_history(user_id):
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                yes_button = types.KeyboardButton('Да')
                no_button = types.KeyboardButton('Нет')
                markup.add(yes_button, no_button)

                # Запрашиваем подтверждение участия в обучении
                msg = bot.send_message(user_id, "Вы подтверждаете участие в обучении?", reply_markup=markup)
                bot.register_next_step_handler(msg, confirm_fin_gram, bot)

            elif check_registration_message_in_history_decl(user_id) and not get_verif_decl_status(user_id):
                sql_query = "UPDATE users SET is_verified_decl = TRUE WHERE id = %s"
                params = (user_id,)
                db_connect.execute_set_sql_query(sql_query, params)
                bot.send_message(message.chat.id, "Подтверждение успешно завершено!")
                menu(bot, message)
            else:
                bot.send_message(message.chat.id, "Регистрация успешно завершена!")
                bot.send_message(message.chat.id, "Если вы хотите изменить информацию то перейдите во вкладку Мой профиль")
                cm_sv_db(message, '/end_register')
                menu(bot, message)

        else:
            raise ValueError("Код не совпадает")  # Исключение, если код не совпадает

    except ValueError as e:
        bot.send_message(message.chat.id, "Неверный код. Попробуйте снова.")
        msg = bot.send_message(message.chat.id, "Введите код еще раз:")
        bot.register_next_step_handler(msg, verify_code, bot)

def send_photo_by_id(message, bot):
    # Проверка, ввел ли пользователь команду выхода в меню
    if message.text.startswith('/'):
        if message.text == '/menu':
            menu(bot, message)
            return

    try:
        # Получаем ID, который ввел пользователь
        photo_id = int(message.text.strip())

        # Получаем изображение из базы данных по ID
        image_data = get_photo_by_id(photo_id)
        if image_data:
            # Отправка фото пользователю
            bot.send_photo(message.chat.id, image_data)
        else:
            bot.reply_to(message, "Фото с таким ID не найдено.")
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректный ID.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

    # Запрос следующего ID фотографии или возвращение в меню
    msg = bot.send_message(message.chat.id, "Введите следующий ID объекта или используйте /menu для выхода в главное меню:")
    bot.register_next_step_handler(msg, send_photo_by_id, bot)
    

def is_none(line):
    if line is None:
        return " "
    return line


def redirect(bot, message, id_i_s=None):
    text = message.text
    if text == "/menu":
        if id_i_s is not None:
            delete_internal_sale(id_i_s)
        menu(bot, message)
        return True
    elif text == "/start":
        if id_i_s is not None:
            delete_internal_sale(id_i_s)
        send_welcome_message(bot, message)
        return True
    return False
