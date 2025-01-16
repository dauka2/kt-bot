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
import hse_competition
import lteClass
import performerClass
import maraphonersClass
import userClass
from appealsClass import set_status, set_date_status, get_appeal_by_id, get_image_data, get_status, set_evaluation, \
    get_appeal_text_all, get_comment, set_comment, set_image_data, add_appeal_gmail, add_appeal, get_appeal_text, \
    set_appeal_text
from commands_historyClass import cm_sv_db
from common_file import (extract_text, extract_number, remove_milliseconds,
                         extract_numbers_from_status_change_decided, generate_buttons, send_gmails, useful_links,
                         check_portal_guide,
                         send_photo_)
from file import check_id, admin_appeal_callback, appeal_inline_markup, admin_appeal, get_user_info, \
    rename_category_to_kaz, rename_category_to_rus
from lteClass import add_internal_sale, set_subscriber_type, set_category_i_s, set_performer_id_i_s, set_is_notified, \
    set_full_name, set_iin, set_phone_num_subscriber, set_subscriber_address, set_product_name, set_action, \
    set_delivery, set_simcard, set_modem, delete_internal_sale
from performerClass import get_performer_by_category, get_regions, list_categories, get_categories_by_parentcategory, \
    get_performer_id_by_category, get_subsubcategories_by_subcategory, \
    get_performer_by_category_and_subcategory, get_performer_by_subsubcategory, get_performers_
from userClass import get_branch, get_firstname, get_user, generate_and_save_code, get_lastname, get_phone_number, get_email, get_table_number, \
set_email, verification_timers, get_saved_verification_code, check_registration_message_in_history, check_if_registered, delete_participation, delete_registration_message_in_history
from user_infoClass import set_appeal_field, get_category_users_info, set_category, get_appeal_field, clear_appeals, \
    set_bool, set_subsubcategory_users_info, get_subsubcategory_users_info

categories_ = ['Learning.telecom.kz | Техникалық қолдау', 'Оқыту | Корпоративтік Университет',
               '"Нысана" қолдау қызметі', 'Комплаенс қызметіне хабарласыңыз',
               'Сатып алу порталы 2.0 | Техникалық қолдау', 'Ашық тендер', 'Баға ұсыныстарын сұрау',
               'Бір дереккөз және электронды дүкен', 'Шарттар жасасу', 'Логистика', 'Тасымалдау']
faq_field = ["Жиі қойылатын сұрақтар", "Демеу", "HR сұрақтары", "Қарыздар бойынша сұрақтар",
             "Сатып алу қызметі бойынша сұрақтар", "Сатып алу порталы бойынша сұрақтар"]
drb_regions = ["Алматинский регион, г.Алматы", "Западный, Центральный регион", "Северный, Южный, Восточный регионы"]
ods_regions = ["ДЭСД 'Алматытелеком'", "Южно-Казахстанский ДЭСД", "Кызылординский ДЭСД", "Костанайский ДЭСД",
               "Восточно-Казахстанский ДЭСД", "Атырауский ДЭСД", "Актюбинский ДЭСД",
               "ДЭСД 'Астана'", "ТУСМ-1", "ТУСМ-6", "ТУСМ-8", "ТУСМ-10", "ТУСМ-11", "ТУСМ-13", "ТУСМ-14", "ГА"]
biot_field = ["👷ҚТ ж ЕҚ кәртішкесін толтыру", "Қауіпті фактор | шарт", "Жұмысты орындау тәртібі", "Ұсыныстар | Идеялар"]
kb_field = ["🗃️Білім базасы", "Нұсқаулық базасы", "Глоссарий", "Пайдалы сілтемелер", "Реттеуші құжаттар"]
kb_field_all = ["Логотиптер және Брендбук", "Жеке кабинет telecom.kz", "Модемдер | Теңшеу", "Lotus | Нұсқаулар",
                "Checkpoint VPN | Қашықтан жұмыс", "Iссапар | Рәсімдеу тәртібі",
                "Қалай кіруге болады", "Жеке профиль", "Порталдан ССП өту", "Филиал серверлері бойынша деректер",
                "Lotus Орнату нұсқаулары", "Lotus орнату файлы", "Қазақтелеком АҚ",
                "Корпоративтік Университет", "Қызметті қалай төлеуге болады",
                "Төлем туралы мәліметтерді қалай көруге болады",
                "Қосылған қызметтерді қалай көруге болады", "'Менің Қызметтерім' Бөлімі", "ADSL модемі",
                "IDTV консолі", "ONT модемдері", "Router 4G and Router Ethernet", "CheckPoint Орнату нұсқаулығы",
                "Checkpoint орнату файлы", "Сатып алу порталы | Нұсқаулар", 'Хатшылар үшін | Нұсқаулар',
                "Бастамашылар | Нұсқаулар үшін", "Абоненттер үшін Wi-Fi сигналын жақсарту",
                "Маршрутизатор мен Mesh жүйесін орнату", "Желі және теледидар+",
                "Желіні орнату және TCP / IP", "ТВ + Қазақтелеком орнату", "Теледидарды Wi-fi желісіне қосу",
                'Өлшеу құралдары',
                'Өлшеу құралдары Нұсқаулық', 'Аннотация өлшеу құралымен жұмыс істеуге арналған нұсқаулық',
                'Қашықтан курстарды оқуға арналған нұсқаулық']
instr_field = ["Брендбук және логотиптер", "Жеке кабинет telecom.kz", "Модемдер | Теңшеу", "Lotus | Нұсқаулар"]
adapt_field = ["😊Welcome курс | Бейімделу", "ДТК", "Общая информация", "Орг структура", "Приветствие", "История",
               "ДТК Инструкции", "Заявки в ОЦО HR", "Заявки возложение обязанностей", "Заявки на отпуск",
               "Командировки", "Переводы", "Порядок оформления командировки", "Рассторжение ТД"]
maraphon_field = ["🚀Цифрлық марафон | Тіркеу"]
fin_gram_field = ['💸"Қаржылық сауаттылық" оқуға тіркелу']
modems_field = ['📶SAPA+']
hse_competition_field = ["👷🏻‍♂️Еңбекті қорғау бойынша конкурстар"]
hse_com_field = ["Мой безопасный рабочий день/Менің қауіпсіз жұмыс күнім", "Лучший совет по безопасности/Ең жақсы қауіпсіздік кеңесі", "Принять участие в обоих конкурсах/Екі байқауға қатысу"]
verification_field = ["📄Декларацияны тапсыруды растау"]
portal_bts = ["'Бірлік' порталы дегеніміз не?", "Порталға қалай кіруге болады?"
    # , "Порталға өтініш қалдыру"
              ]
sapa_admin = ['1066191569', '353845928', '947621727', '468270698', '531622371', '1621516433', '477945972', '577247261', '735766161', '476878708', '597334185', '559872057', '510122980']
# "Бірлік Гид"
portal_ = ["Мобильді нұсқа", "ДК немесе ноутбук", "Қалай кіруге болады", "Жеке профиль", "Порталдан ССП өту",
           "iOS", "Android", "Есть checkpoint", "Нет checkpoint"]
portal_guide = ["Кері байланыс үшін қайда жүгіну керек-пікірлер мен ұсыныстар?",
                "Порталда компанияның стратегиясымен қайдан танысуға болады?",
                "Қауымдастықты қалай құруға болады?", "Экожүйеде демалысты қалай жоспарлауға болады?",
                "Әріптесіңізге қалай алғыс айтамын?", "Экожүйеде сауалнаманы қалай құруға болады?",
                "Қазақтелеком дүкенінен жеңілдікпен тауарды қалай сатып алуға болады?",
                "Қазақтелеком саудасын қалай сатып алуға болады?",
                "Компания қызметкерлеріне жеңілдіктер мен акцияларды қайдан көруге болады?"]
lte_ = ['🛜 Акция "Пилот LTE"', "Об акции", "А как продать?", "Отправить заявку", "Мои продажи"]
pp = ['ALEM PLUS (1 год) c Bereke 2', 'ALEM PLUS (1 год) c Bereke 1', 'ALEM PLUS (без контракта) c Bereke 1',
      'ALEM PLUS (без контракта) c Bereke 2', 'ALEM TV (без контракта)', 'ALEM TV (1 год)',
      'ALEM MOBILE (без контракта) c Bereke 1', 'ALEM MOBILE (без контракта) c Bereke 2',
      'ALEM MOBILE (1 год) c Bereke 1', 'ALEM MOBILE (1 год) c Bereke 2', 'ТП Алем']
faq_1 = {
    'Қазақтелеком "АҚ-да "Демеу" бағдарламасы кімге бағытталған?':
        'Қазақтелеком" АҚ "Демеу" бағдарламасын әлеуметтік қолдау: (бұдан әрі-Бағдарлама) жұмыскерлерге мәртебесі '
        'бойынша жіберілді: \
    \n1) Көп балалы отбасы-өз құрамында төрт және одан да көп бірге тұратын кәмелетке толмаған балалары, оның ішінде '
        'кәмелетке толғаннан кейін орта, техникалық және кәсіптік, орта білімнен кейінгі, жоғары және (немесе) жоғары '
        'оқу орнынан кейінгі білім беру ұйымдарында күндізгі оқу нысаны бойынша білім алатын балалары бар отбасы  \
    отбасы (бірақ білім алуды аяқтағанға дейін) жиырма үш жасқа толған жетістіктер);  \
    \n2) Мүгедек балалары бар отбасы-өз құрамында он сегіз жасқа дейінгі баласы (балалары) бар, бар, '
        'тұрмыс-тіршілігінің шектелуіне және оны әлеуметтік қорғау қажеттігіне әкеп соқтыратын, ауруларға, мертігулерге'
        ' (жаралануға, жарақаттарға, контузияларға), олардың зардаптарына, кемістіктерге байланысты ағзаның қызметінде'
        ' тұрақты бұзылуы бар отбасын (оларды) әлеуметтік қорғау; \
    \n3) 2-ден астам бала асырап алған/асырап алған отбасы - құрамында 2-ден астам кәмелетке толмаған асырап алған/'
        'асырап алынған балалары бар, денсаулық жағдайы бойынша диспансерлік есепте тұрған және жалғыз асыраушысы '
        'бар отбасы.\
    \n4) A8-B4 грейдінің жұмыскерлеріне балаларының орта арнаулы оқу орнында (бұдан әрі - CYZ) жоғары оқу орнында '
        '(бұдан әрі - BYZ) түлектердің оқу курсына (тұруға және тамақтануға арналған шығыстарды есептемегенде) ақы '
        'төлеу бойынша әлеуметтік қолдау белгіленеді. Барлық әлеуметтік қолдау түрлері әлеуметтік қолдау көрсету '
        'мерзімінде Қоғамда кемінде 3 жыл үздіксіз жұмыс өтілі бар Қоғам жұмыскерлеріне көрсетіледі.',
    'Жұмыскерлерге әлеуметтік қолдау түрлері':
        '1) балалардың сауықтыру лагерьлеріне жолдамалар сатып алуға байланысты шығыстарды өтеу; \
    \n2) Балалардың сауықтыру санаторийлеріне (мүгедек балалар үшін) жолдамалар сатып алуға байланысты '
        'шығыстарды өтеу; \
    \n3) Балаларға арналған дәрілік заттарды сатып алуға материалдық көмек; \
    \n4) Мектеп оқушыларының тамақтануына материалдық көмек; \
    \n5) Оқу жылының басына материалдық көмек; \
    \n6) Медициналық оңалту/баланы оңалтудың жеке бағдарламасы үшін қаражатты өтеу (мүгедек балалар үшін); \
    \n7) Арнайы білім беру бағдарламалары үшін қаражатты өтеу (мүгедек балалар үшін); \
    \n8) Арнайы түзету ұйымдарына барғаны үшін қаражатты өтеу (мүгедек балалар үшін); \
    \n9) Мектеп бітірген күні кәмелетке толмаған және оқуын өте жақсы бітірген мектеп түлектеріне материалдық көмек; \
    \n10) Орта арнаулы оқу орнында (бұдан әрі-CYZ)/жоғары оқу орнында (бұдан әрі - BYZ) балаларының бітіруші оқу курсын'
        ' (тұруға және тамақтануға арналған шығыстарды есептемегенде) төлеу жөніндегі шығыстарды (A8 - B4 грейд '
        'қызметкерлеріне) өтеу.',
    'Әлеуметтік комиссияға өтініш беру үдерісі':
        'Филиалдың әлеуметтік комиссиясына өтінішті ресімдеу - др. ДРБ әлеуметтік комиссиясының төрағасы-Погребицкий'
        ' И. Е. әлеуметтік қолдау көрсету үшін қоғам қызметкерлері жүгінген кезде өтініштерді қараудың кезектілік '
        'тәртібі сақталады.',
    'Өтінішті қайда рәсімдеу керек?':
        'Сіз өзіңіздің жұмыс базаңызда(BRD) өтініш жасайсыз. Арнайы базалар жоқ.',
    'Әлеуметтік комиссияның төрағасы': 'Филиалдардағы әлеуметтік комиссияның төрағасы-филиалдың бас директоры. '
                                       'ОА-операциялық тиімділік жөніндегі Бас директор',
}
faq_2 = {
    'Жұмыс орнынан анықтаманы қалай алуға болады?':
        'Жұмыс орнынан анықтама алуға өтінімді "HR ОҚО өтінімдері" базасында ресімдеу қажет. Жаңасын '
        'жасаңыз-филиалыңыздың атауын таңдаңыз - жұмыс орнынан анықтама беруге өтінім – жұмыскердің аты – жөнін, '
        'анықтама түрін және қажетті өлшемдерді толтырыңыз (тілі, өтілі, лауазымдық жалақысы, орташа жалақысы) – '
        'өтінімді сақтаңыз-өтінімді ОҚО-ға жіберіңіз өтінімде сіздің өтініміңіздің орындаушысы автоматты түрде '
        'көрсетіледі.',
    'Lotus Notes есептік жазбасын құру және ИС  және ЖҚБ-ға кіруге болады?':
        'Lotus Notes есептік жазбасын құру үшін  өзіңіздің жетекшілік ететін құрылымдық бөлімшенің басшысына/'
        'тәлімгеріне/іс жүргізушісіне ҚББЖ  (қатынауды басқарудың бірыңғай жүйесі) өтінімді ресімдеу үшін жүгінуіңіз '
        'керек. \nПо есептік жазбаның дайындығына қарай (логині мен паролі бар файл) Help Desk-ке келесі нөмір бойынша '
        'өтінім беру қажет: +7 727 2587304 Lotus Notes есептік жазбасын орнатқаннан кейін, сіз үшін АЖ және ДҚ-ға '
        'қажетті қол жетімділікті көрсете отырып, ҚББЖ базасында өтінімді өз бетіңізше жасау қажет.',
    'Егер сіз Lotus паролін немесе ақауын ұмытып қалсаңыз, қайда барасыз?':
        'Туындаған мәселелер бойынша Help Desk +77272587304 өтінімін қалдырыңыз.',
    'Аурухана парақтары жұмысшыларға төлене ме?':
        '1) компаниядағы үздіксіз жұмыс өтіліне байланысты қызметкерлер (кәсіподақ ұйымының мүшелері және ұжымдық '
        'ұйымға қосылған) үшін (5 жасқа дейін - орташа жалақының 40%, 5 жылдан астам - еңбекке уақытша жарамсыздық '
        'күндері үшін орташа жалақының 70%);\n2) қалған қызметкерлер үшін - заңнамада белгіленген мөлшерде.\n3) Еңбекке'
        ' уақытша жарамсыздық парағы / o парағы',
    'Еңбекке жарамсыздық парағын кім толтырады?':
        'Еңбекке жарамсыздық парағын құрылымдық бөлімшенің  табельшісі/іс жүргізушісі толтырады. Еңбекке жарамсыздық '
        'парағында "Қазақтелеком" АҚ филиалы - "Бөлшек бизнес жөніндегі дивизион" -  филиалының атауы және өз лауазымы'
        ' көрсетіледі.',
    'Еңбекке уақытша жарамсыздық парағын кімге тапсыру керек (аурухана парағы)':
        'Еңбекке уақытша жарамсыздық парағын тапсырар алдында оны толтырып, оның тікелей жетекшісі қол қою керек, '
        'егер сіздің кеңсеңізде OҚO HR фронт-офисінің жұмыскері болмаса - BL екі жағынан сканерлеп, OҚO HR өтінім '
        'базасында өтінім ресімдеңіз; әйтпесе-толтырылған BL түпнұсқасын OҚO HR фронт-офисінің жұмыскеріне '
        'тапсырыңыз.',
    'Әріптестердің телефонын қайдан табуға болады?':
        'Әріптестің телефонын  Қоғамның "Телефон анықтамалығы" базасынан таба аласыз-телефон нөмірлері, жұмыскерлерді '
        'бөлім бойынша іздеу',
    'Айналып өту парағы. Ол қашан ресімделеді?':
        '1) Жұмыстан босату туралы өтінішті ресімдегенде, үшінші парақта автоматты түрде кету парағы жасалады және қол'
        ' қоюшылар көрсетіледі.\n2) филиалға/біржақты тәртіппен/ ауыстыру кезінде кету парағын өз жұмыс '
        'базаларында ресімделеді,'
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
        'Порядок осуществления закупок акционерным обществом «Фонд национального благосостояния «Самрук-Қазына» и '
        'юридическими лицами, пятьдесят и более процентов голосующих акций (долей участия) которых прямо или косвенно '
        'принадлежат АО «Самрук-Қазына» на праве собственности или доверительного управления и Регламент взаимодействия'
        ' Дирекции «Телеком Комплект» с филиалами АО «Казахтелеком».',
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
        'Пул товаров всех ПК Фонда, в которых имеется постоянная и стабильная востребованность группы компаний, '
        'но отсутствует производство в стране.',
    'Как определяется маркетинговая цена?':
        'Маркетинговая цена - цена на товар, применяемая заказчиком для формирования бюджетов расходов/плана(ов) '
        'закупок и не включающая в себя налог на добавленную стоимость. Маркетинговые цены на товары определяются в '
        'соответствии с Приложением № 3 к Порядку."'

}
branches = ['Центральный Аппарат', 'Обьединение Дивизион "Сеть"', 'Дивизион по Розничному Бизнесу',
            'Дивизион по Корпоративному Бизнесу', 'Корпоративный Университет', 'Дивизион Информационных Технологий',
            'Дирекция Телеком Комплект', 'Дирекция Управления Проектами',
            'Сервисная Фабрика']

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
#     # {'branch': 'Центральный Аппарат', 'sapa_admin': '735766161'},
#     {'branch': 'Центральный Аппарат', 'sapa_admin': '559872057'},
#     # {'branch': 'Центральный Аппарат', 'sapa_admin': '1009867354'},
#     # {'branch': 'Обьединение Дивизион "Сеть"', 'sapa_admin': '1621516433'},
#     {'branch': 'Обьединение Дивизион "Сеть"', 'sapa_admin': '735766161'},
#     {'branch': 'Дивизион по Розничному Бизнесу', 'sapa_admin': '531622371'},
#     {'branch': 'Дивизион по Корпоративному Бизнесу', 'sapa_admin': '468270698'},
#     {'branch': 'Корпоративный Университет', 'sapa_admin': '476878708'},
#     {'branch': 'Дивизион Информационных Технологий', 'sapa_admin': '577247261'},
#     {'branch': 'Дирекция Телеком Комплект', 'sapa_admin': '597334185'},
#     {'branch': 'Дирекция Управления Проектами', 'sapa_admin': '947621727'},
#     {'branch': 'Сервисная Фабрика', 'sapa_admin': '477945972'}
# ]

branches_admin = 735766161
# branches_admin = 1066191569

def get_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    if check_id(str(message.chat.id)):
        markup.add(types.KeyboardButton("Админ панель"))
    # button1 = types.KeyboardButton(hse_competition_field[0])
    # button2 = types.KeyboardButton("🚀Цифрлық марафон | Тіркеу")
    button10 = types.KeyboardButton('📶SAPA+')
    button9 = types.KeyboardButton("📄Декларацияны тапсыруды растау")
    button = types.KeyboardButton("😊Welcome курс | Бейімделу")
    button3 = types.KeyboardButton("🗃️Білім базасы")
    button4 = types.KeyboardButton("👷ҚТ ж ЕҚ кәртішкесін толтыру")
    button5 = types.KeyboardButton("📄Менің сұрағым бар")
    button6 = types.KeyboardButton("🧐Менің профилім")
    button7 = types.KeyboardButton('🖥Портал "Бірлік"')
    button8 = types.KeyboardButton(lte_[0])
    markup.add(button10, button9, button)
    #markup.add(button1, button9, button2, button)
    if get_branch(message.chat.id) == branches[2]:
        markup.add(button8)
    markup.add(button3, button7, button5, button4, button6)
    return markup


def send_welcome_message(bot, message):
    welcome_message = f'Сәлем {get_firstname(message)}👋'
    markup = get_markup(message)
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    send_photo_(bot, message.chat.id, "images/menu.jpg")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Менің сценарийімде бірнеше пәрмендер бар:\
        \n/menu — негізгі мәзірге оралу (сіз мұны демонстрация кезінде кез келген уақытта жасай аласыз!)\
        \n/help - әзірлеушілермен байланысыңыз (егер қиындықтарға тап болсаңыз немесе сізде жақсарту үшін ұсыныстар "
                                      "болса, осы пәрменді қолданыңыз) \
        \n/start — ботты қайта іске қосыңыз\
        \n/language - боттың тілін өзгерту\
        \n\n Пәрмендерді /menu бөлігіндегі хабарламалар жолағынан таба аласыз (төменгі сол жақта) "
                                      "немесе жай ғана пәрменнің атауына, '/' ұмытпаңыз! белгісіне келіңіз.")


regions_ = ["Астана қаласы", "Алматы қаласы", "Шымкент қаласы", "Ақтөбе қаласы", "Қарағанды облысы", "Абай облысы",
            "Ақмола облысы", "Ақтөбе облысы", "Қарағанды қаласы", "Алматы облысы", "Атырау облысы",
            "Батыс Қазақстан облысы", "Жамбыл облысы", "Жетісу облысы", "Қостанай облысы", "Қызылорда облысы",
            "Маңғыстау облысы", "Павлодар облысы", "Солтүстік Қазақстан облысы", "Түркістан облысы",
            "Ұлытау облысы", "Шығыс Қазақстан облысы"]


def send_error(bot, message):
    common_file.send_photo_(bot, message.chat.id, 'images/oops_error kaz.jpg')
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Ой, бірдеңе дұрыс болмады... /menu түймесін басу арқылы ботты қайта іске қосып көріңіз")


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
    if message_text == '💸"Қаржылық сауаттылық" оқуға тіркелу':
        # Проверяем статус пользователя
        is_verified = userClass.get_user_verification_status_reg(user_id)
        add_message_to_history(user_id, message_text)
        if not is_verified:
            # Если пользователь не верифицирован, просим ввести корпоративную почту
            msg = bot.send_message(user_id, "Тексеру үшін 4 таңбалы код жіберілетін корпоративтік электрондық поштаңызды растау қажет. \nЭлектрондық поштаңызды енгізіңіз. \nMысалы :User.U@telecom.kz")
            bot.register_next_step_handler(msg, process_email_kaz, bot)
        elif check_registration_message_in_history(user_id) and check_if_registered(user_id):
            # Создаем клавиатуру с кнопками "Да" и "Нет"
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            yes_button = types.KeyboardButton('Иә')
            no_button = types.KeyboardButton('Жоқ')
            markup.add(yes_button, no_button)

            # Запрашиваем подтверждение участия в обучении
            msg = bot.send_message(user_id, "Сіз бұл тренингке тіркелдіңіз бе, жазбаны жойғыңыз келе ме?",
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, delete_fin_gram, bot)
        else:
            # Создаем клавиатуру с кнопками "Да" и "Нет"
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            yes_button = types.KeyboardButton('Иә')
            no_button = types.KeyboardButton('Жоқ')
            markup.add(yes_button, no_button)

            # Запрашиваем подтверждение участия в обучении
            msg = bot.send_message(user_id, "Сіз бұл тренингке қатысқыңыз келетінін растайсыз ба?",
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, confirm_fin_gram_kaz, bot)

def delete_fin_gram(message, bot):
    user_id = message.chat.id
    response = message.text.strip().lower()

    if response == 'иә':
        delete_participation(message)
        delete_registration_message_in_history(user_id)
        clear_message_history(user_id)

        # Отправляем сообщение о успешном удалении
        bot.send_message(user_id, "Сіз оқудан шығарылдыңыз")
        menu(bot, message)
    elif response == 'жоқ':
        # Отправляем сообщение об отмене регистрации и возвращаем в главное меню
        bot.send_message(user_id, "Жою жойылды.")
        menu(bot, message)
    else:
        # Обработка неверного ввода, если вдруг пришел текст не "Да" и не "Нет"
        msg = bot.send_message(user_id, "'Иә' немесе 'Жоқ' таңдаңыз.")
        bot.register_next_step_handler(msg, confirm_fin_gram_kaz, bot)

def confirm_fin_gram_kaz(message, bot):
    user_id = message.chat.id
    response = message.text

    if response == 'Иә':
        # Добавляем запись в таблицу financial_literacy
        webinar_name = "Финансовая грамотность"
        sql_query = "INSERT INTO financial_literacy (user_id, webinar_name) VALUES (%s, %s)"
        params = (user_id, webinar_name)
        db_connect.execute_set_sql_query(sql_query, params)

        # Отправляем сообщение о успешной регистрации
        bot.send_message(user_id, "Сіз қаржылық сауаттылық бойынша оқуға сәтті тіркелдіңіз!")
        menu(bot, message)

    elif response == 'Жоқ':
        # Отправляем сообщение об отмене регистрации и возвращаем в главное меню
        bot.send_message(user_id, "Тіркеу тоқтатылды.")
        menu(bot, message)
    else:
        # Обработка неверного ввода, если вдруг пришел текст не "Да" и не "Нет"
        msg = bot.send_message(user_id, '"Иә" немесе " Жоқ " таңдаңыз.')
        bot.register_next_step_handler(msg, confirm_fin_gram_kaz, bot)

def verification(bot, message, message_text):
    user_id = message.chat.id
    if message_text == "📄Декларацияны тапсыруды растау":
        add_message_to_history(user_id, message_text)
        bot.send_message(message.chat.id, "Осы батырманы басу арқылы сіз декларацияны форма бойынша растайсыз - "
                                          "салық есептілігі 270.00, тапсырылды")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        yes_button = types.KeyboardButton('Иә')
        no_button = types.KeyboardButton('Жоқ')
        markup.add(yes_button, no_button)
        is_verified_decl = userClass.get_user_verification_status(user_id)
        is_verified = userClass.get_user_verification_status_reg(user_id)
        # bot.send_message(message.chat.id, str(is_verified_decl))
        if not is_verified:
            # Если пользователь не верифицирован, запрашиваем почту
            msg = bot.send_message(user_id, "Тексеру үшін 4 таңбалы код жіберілетін корпоративтік электрондық поштаңызды растау қажет. \nэлектрондық поштаңызды енгізіңіз. \n мысалы :User.U@telecom.kz")
            bot.register_next_step_handler(msg, process_email_kaz, bot)
        elif not is_verified_decl and userClass.check_registration_message_in_history_decl_kaz(user_id):
            # Если пользователь не верифицирован, просим ввести корпоративную почту
            msg = bot.send_message(user_id, "Сіз декларацияны тапсырғаныңызды растайсыз ба?", reply_markup=markup)
            bot.register_next_step_handler(msg, process_declaration_confirmation, bot)
        else:
            bot.send_message(user_id, "Сіз өзіңіздің поштаңызды тексеріп, декларацияға қол қойғаныңызды растадыңыз")
            menu(bot, message)

def process_declaration_confirmation(message, bot):
    user_id = str(message.chat.id)
    response = message.text.strip().lower()  # Приводим ответ к нижнему регистру для проверки

    if response == 'иә':
        # Если ответ "Да", обновляем статус в базе данных
        sql_query = "UPDATE users SET is_verified_decl = TRUE WHERE id = %s"
        params = (user_id,)
        try:
            # Выполняем SQL-запрос
            db_connect.execute_set_sql_query(sql_query, params)
            bot.send_message(user_id, "Декларацияның тапсырылғанын растау сәтті аяқталды!")
            menu(bot, message)
        except Exception as e:
            # Ловим возможные ошибки и выводим их для отладки
            bot.send_message(user_id, f"Произошла ошибка при обновлении статуса: {e}")

    elif response == 'жоқ':
        # Если ответ "Нет", возвращаем пользователя в главное меню
        bot.send_message(user_id, "Сіз декларацияны растаудан бас тарттыңыз.")
        menu(bot, message)

    else:
        # Если введен некорректный ответ, просим повторить
        msg =bot.send_message(user_id, "Опциялардың бірін таңдаңыз: 'Иә' немесе 'Жоқ'.")
        bot.register_next_step_handler(msg, process_declaration_confirmation, bot)

def process_email_kaz(message, bot):
    user_id = str(message.chat.id)
    regex = r'\b[A-Za-z0-9._%+-]+@telecom.kz\b'
    # Получаем email пользователя из сообщения
    email = message.text
    set_email(message, email)

    if redirect(bot, message, id_i_s = None):
        return

    elif email:
        # Проверка на корпоративный email
        if re.fullmatch(regex, email):
            # Отправляем код подтверждения на email пользователя, передаем bot и chat_id
            send_verification_code(user_id, bot, message)
            msg = bot.send_message(message.chat.id,
                                   f"Растау үшін 5 минут ішінде жұмыс поштаңызға жіберілген кодты енгізіңіз.\n\nСізге жіберілген кодты енгізу арқылы сіз жеке деректерді жинауға және өңдеуге келісім бересіз")
            bot.register_next_step_handler(msg, verify_code_kaz, bot)
        else:
            # Если email не корпоративный, уведомляем пользователя и повторно запрашиваем email
            msg = bot.send_message(message.chat.id,
                                   "Енгізілген электрондық пошта мекенжайы корпоративтік емес. Сізден дұрыс корпоративтік e-mail-ді тағы бір рет енгізуіңізді сұраймыз.")
            bot.register_next_step_handler(msg, process_email_kaz, bot)
    else:
        bot.send_message(message.chat.id,
                         "Сіздің поштаңызды табу мүмкін болмады. Дұрыс электрондық поштаны енгізгеніңізге көз жеткізіңіз.")


def start_verification_timer(user_id, bot, message):
    # Таймер на 5 минут (300 секунд)
    def timer():
        time.sleep(300)  # Ожидание 5 минут
        if user_id in verification_timers:
            del verification_timers[user_id]  # Удаляем таймер по истечению времени
            sql_query = "UPDATE users SET email = NULL WHERE id = %s"
            params = (user_id,)
            db_connect.execute_set_sql_query(sql_query, params)
            bot.send_message(message.chat.id, "Күту уақыты аяқталды.")
            msg = bot.send_message(message.chat.id, "Корпоративтік e-mail енгізіңіз:")
            bot.register_next_step_handler(msg, process_email_kaz, bot)
            return

    # Создаем и запускаем поток для таймера
    verification_timers[user_id] = threading.Thread(target=timer)
    verification_timers[user_id].start()

def sapa_con(bot, message):
    user_id = message.chat.id
    message_text = message.text

    if message_text == '📶SAPA+':
        # Основное меню с двумя кнопками
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'), types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

        bot.send_message(user_id, "Әрекеттердің бірін таңдаңыз:", reply_markup=markup)
        bot.register_next_step_handler(message, sapa_main_menu, bot)


def sapa_main_menu(message, bot):
    user_id = message.chat.id
    choice = message.text.strip().lower()

    if choice.startswith('/'):
        # Переход в меню, если команда "/menu"
        if choice == '/menu':
            menu(bot, message)
            return True
    elif choice == 'sapa+ бонустық жүйесі':
        # Меню с действиями для администратора и участников
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        if str(user_id) in sapa_admin:
            markup.add(types.KeyboardButton('Сілтемелерді бағалау'), types.KeyboardButton('Кестені жүктеу'))
        else:
            markup.add(types.KeyboardButton('Сілтемені/фотосуретті жүктеу'))
        markup.add(types.KeyboardButton('Көшбасшылар тақтасы'), types.KeyboardButton('Артқа'))

        bot.send_message(user_id, "Мәзірдегі әрекеттердің бірін таңдаңыз:", reply_markup=markup)
        bot.register_next_step_handler(message, sapa_instruments, bot)

    elif choice == 'нұсқаулар, техникалық қолдау және табыстау нүктелері':
        # Меню с четырьмя дополнительными кнопками
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Модемді орнату бойынша нұсқаулық'))
        markup.add(types.KeyboardButton('Sapa+ маршрутизаторларын беру пункттері'))
        markup.add(types.KeyboardButton('SAPA+QUEST'))
        # markup.add(types.KeyboardButton('Техникалық мәселелер бойынша чат боты/ ОДС'))
        markup.add(types.KeyboardButton('SAPA+ абоненттерін тексеру'), types.KeyboardButton('Мегалайнерлерге арналған SAPA+ қолдауы'))
        # markup.add(types.KeyboardButton('SAPA+ ДТПК орнату/жылдамдық бойынша көмек'), types.KeyboardButton('SAPA+ абоненттерін тексеру'))

        bot.send_message(user_id, "Міне, қажетті ақпарат:", reply_markup=markup)
        bot.register_next_step_handler(message, additional_info_handler, bot)

    else:
        # Если пользователь ввел что-то другое, попросим сделать выбор снова
        bot.send_message(user_id, "Ұсынылған опциялардан әрекетті таңдаңыз.")
        bot.register_next_step_handler(message, sapa_main_menu, bot)

def sapa_instruments(message, bot):
    user_id = str(message.chat.id)
    response = message.text.strip().lower()

    if response.startswith('/'):
        # Переход в меню, если команда "/menu"
        if response == '/menu':
            menu(bot, message)
            return True
    elif response == 'көшбасшылар тақтасы':
        display_leaderboard(bot, message)
    elif response == 'сілтемелерді бағалау' and str(user_id) in sapa_admin:
        show_pending_links(message, bot)
    elif response == 'кестені жүктеу' and str(user_id) in sapa_admin:
        # msg = bot.send_message(user_id, "Қатысушының деректері бар Excel файлын жүктеңіз.")
        # bot.register_next_step_handler(msg, upload_sapa_table, bot)
        bot.send_message(message.chat.id, "Әлі дамуда...")
        bot.send_message(message.chat.id, "'/menu'-деп жазып негізгі мәзірге оралыңыз.")
    elif response == 'сілтемені/фотосуретті жүктеу':
        msg = bot.send_message(user_id, "Сілтемені/фотосуретті жіберіңіз:")
        bot.register_next_step_handler(msg, upload_link, bot)
    elif response == 'артқа':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'),
                   types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

        msg = bot.send_message(user_id, "Опциялардың бірін таңдаңыз", reply_markup=markup)
        bot.register_next_step_handler(msg, sapa_main_menu, bot)
    else:
        bot.send_message(user_id, "Опциялардың бірін таңдаңыз.")
        bot.register_next_step_handler(message, sapa_instruments, bot)

def additional_info_handler(message, bot):
    user_id = message.chat.id
    info_request = message.text.strip().lower()

    # Обработка кнопок "необходимая информация"
    if info_request.startswith('/'):
        if info_request == '/menu':
            menu(bot, message)
            return True
    elif info_request == 'модемді орнату бойынша нұсқаулық':
        bot.send_message(user_id, "Роутерді баптау бойынша бейненұсқаулық:\nhttps://youtu.be/mpDbJNkRS04")
        bot.send_message(user_id, "Мегалайнерге арналған нұсқаулық. Абонент үшін маршрутизаторды орнатуға көмек https://youtu.be/0e4Yc5Kdzpo")
        bot.send_document(user_id, open("files/Инструкция_по_подключению_и_настройке_роутера.pdf", 'rb'))
        bot.send_document(user_id, open("files/Создание_заявки_мегалайнером+смс_6_тизначный.pdf", 'rb'))
        bot.send_document(user_id, open("files/Создание заявки мегалайнером.pdf", 'rb'))
        bot.send_document(user_id, open("files/Инструкция_пользователя_WFM_инсталлятор.pdf", 'rb'))
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
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'sapa+ маршрутизаторларын беру пункттері':
        bot.send_document(user_id, open("files/Пункты_выдачи_и_обучение_мегалайнеров_SAPAplus.pdf", 'rb'))
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'техникалық мәселелер бойынша чат боты/ одс':
        bot.send_message(user_id, "Ботқа қосылу сілтемесі: https://t.me/C_M_S_bot")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'мегалайнерлерге арналған sapa+ қолдауы':
        bot.send_message(user_id, "Группаға қосылу үшін сілтеме: https://t.me/+gCyDTZGRZIBlZDIy")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'sapa+quest':
        bot.send_message(user_id, "Ақпараттық арнаға сілтеме: https://t.me/+LJl92t3A3NE2MzMy")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'sapa+ дтпк орнату/жылдамдық бойынша көмек':
        bot.send_message(user_id, "Ссылка для присоединения к группе: https://t.me/+yVOT2YdR6hAyMjRi")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    elif info_request == 'sapa+ абоненттерін тексеру':
        bot.send_message(user_id, "Ссылка для присоединения к группе: https://t.me/+b2lri21NwEM3YmRi")
        bot.register_next_step_handler(message, additional_info_handler, bot)
    else:
        bot.send_message(user_id, "Опциялардың бірін таңдаңыз.")
        bot.register_next_step_handler(message, additional_info_handler, bot)

def links_instruments(message, bot):
    user_id = str(message.chat.id)
    response = message.text.strip().lower()

    if response.startswith('/'):
        # Переход в меню, если команда "/menu"
        if response == '/menu':
            menu(bot, message)
            return True
    elif response == 'жүктеу':
        msg = bot.send_message(user_id, "Сілтемені/фотосуретті жіберіңіз:")
        bot.register_next_step_handler(msg, upload_link, bot)
    elif response == 'тексерілмеген сілтемелер тізімі':
        show_user_links(bot, message)
    else:
        bot.send_message(user_id, "Опциялардың бірін таңдаңыз.")
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
            bot.send_message(user_id, "Сілтемелерді жүктеу процесі аяқталды.")
            msg = bot.send_message(user_id, "Төменде қол жетімді опциялардың бірін таңдаңыз:")
            bot.register_next_step_handler(msg, links_instruments, bot)
            return

        if not link.startswith("http"):
            bot.send_message(user_id, "Қате сілтеме пішімі. Дұрыс URL мекенжайын көрсетіңіз.")
            msg = bot.send_message(user_id, "Сілтеме / фотосурет жіберіңіз:")
            bot.register_next_step_handler(msg, upload_link, bot)
            return

        try:
            user_info = get_user(message.chat.id)
            email = user_info[6]
            branch = user_info[7]
            if not email or not branch:
                bot.send_message(user_id, "Қате: email немесе филиал табылмады.")

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

            bot.send_message(user_id, "Сілтеме сәтті жүктелді! Тексеруді күтіңіз.")

            bot.send_message(user_id, "Сіз Sapa+ негізгі мәзіріне бағытталасыз")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'),
                       types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

            msg = bot.send_message(user_id, "Опциялардың бірін таңдаңыз", reply_markup=markup)
            bot.register_next_step_handler(msg, sapa_main_menu, bot)
        except Exception as e:
            bot.send_message(user_id, f"Сілтемені жүктеу кезінде қате пайда болды: {e}")

    # Обработка фото
    elif message.photo:
        bot.send_message(user_id, "Фотосурет алынды, біз жүктеуді бастаймыз...")
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            file_url = f'https://api.telegram.org/file/bot{db_connect.TOKEN}/{file_info.file_path}'

            response = requests.get(file_url)
            if response.status_code == 200:
                file_data = response.content
            else:
                bot.send_message(user_id, "Фотосуретті жүктеу кезінде қате пайда болды. Қайталап көріңіз.")
                return

            user_info = get_user(message.chat.id)
            email = user_info[6]
            branch = user_info[7]
            if not email or not branch:
                bot.send_message(user_id, "Қате: email немесе филиал табылмады.")
                return

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

            bot.send_message(user_id, "Фотосурет сәтті жүктелді және тексеруді күтуде.")

            bot.send_message(user_id, "Сіз Sapa+ негізгі мәзіріне бағытталасыз")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'),
                       types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

            msg = bot.send_message(user_id, "Опциялардың бірін таңдаңыз", reply_markup=markup)
            bot.register_next_step_handler(msg, sapa_main_menu, bot)

        except Exception as e:
            bot.send_message(user_id, f"Фотосуретті жүктеу кезінде қате пайда болды: {e}")
    else:
        bot.send_message(user_id, "Сілтеме немесе фотосурет жіберіңіз.")
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
        bot.send_message(message.chat.id, "Сіздің электрондық поштаңыз табылмады.")
        return

    links_result = db_connect.execute_get_sql_query(
        "SELECT link, status FROM sapa_link WHERE email = %s AND is_checked = FALSE", (user_email,)
    )

    if links_result:
        response_message = "Сіздің сілтемелеріңіз және олардың күйлері:\n"
        for link, status in links_result:
            response_message += f"Сілтеме: {link}\nЖағдайы: {status}\n\n"
        
        bot.send_message(message.chat.id, response_message)
        bot.send_message(message.chat.id, "Сіз Sapa+ негізгі мәзіріне бағытталасыз")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'),
                   types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

        msg = bot.send_message(message.chat.id, "Әрекеттердің бірін таңдаңыз:", reply_markup=markup)
        bot.register_next_step_handler(msg, sapa_main_menu, bot)
    else:
        msg = bot.send_message(message.chat.id, "Қазіргі уақытта сізде тексеруді күтетін сілтемелер жоқ.")
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
    leaderboard = "Көшбасшылар тақтасы:\n" + "\n".join(
        f"{i}. Қатысушы {row[0]} - Жалпы балл: {row[1]}"
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
            bot.send_message(message.chat.id, f"Сіздің орныңыз: {user_rank}, Жалпы балл: {user_score}")
        else:
            bot.send_message(message.chat.id, "Сіз әлі байқауға қатыспайсыз.")
    else:
        bot.send_message(message.chat.id, "Сіздің электрондық поштаңызды табу мүмкін болмады.")

    # Переход к доступным опциям 
    bot.send_message(message.chat.id, "Біз сізді Sapa+ негізгі мәзіріне бағыттаймыз")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'),
               types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

    msg = bot.send_message(message.chat.id, "Әрекеттердің бірін таңдаңыз:", reply_markup=markup)
    bot.register_next_step_handler(msg, sapa_main_menu, bot)

# Функция для отображения ссылок для администратора с фильтрацией по branch
def show_pending_links(message, bot):
    try:
        if message.chat.id != branches_admin:
            bot.send_message(message.chat.id, "Қате: әкімші филиалы табылмады.")
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
                    bot.send_message(message.chat.id, f"Сілтеме: {link}")
                elif image_data:
                    bot.send_photo(message.chat.id, image_data)

                # Инлайн-клавиатура для оценок
                markup = types.InlineKeyboardMarkup(row_width=2)
                buttons = [
                    types.InlineKeyboardButton("Қызметкердің посты/сторис", callback_data=f'пост {link_id}'),
                    types.InlineKeyboardButton("Клиенттің посты/сторис", callback_data=f'пост1 {link_id}'),
                    types.InlineKeyboardButton("Пікір", callback_data=f'отзыв {link_id}'),
                    types.InlineKeyboardButton("Ештеңе", callback_data=f'ничего {link_id}')
                ]
                markup.add(*buttons)

                bot.send_message(message.chat.id, "Әрекетті таңдаңыз:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Қазіргі уақытта тексеру үшін жаңа сілтемелер немесе фотосуреттер жоқ.")
            msg = bot.send_message(message.chat.id, "Төменде қол жетімді опциялардың бірін таңдаңыз:")
            bot.register_next_step_handler(msg, sapa_instruments, bot)
    except Exception as e:
        bot.send_message(message.chat.id, f"Сілтемелерді алу кезінде қате: {e}")

def upload_sapa_table(message, bot):
    bot.send_message(message.chat.id, "Әлі де дамуда...")
    bot.send_message(message.chat.id, "'/menu'-деп жазып негізгі мәзірге оралыңыз.")
    
    '''
    user_id = str(message.chat.id)
    if message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        try:
            # Загружаем данные из Excel файла в DataFrame
            df = pd.read_excel(io.BytesIO(downloaded_file))

            # Очищаем таблицу sapa и вставляем новые данные
            db_connect.execute_set_sql_query("DELETE FROM sapa")
            for _, row in df.iterrows():
                # Вставка данных в таблицу sapa
                insert_sapa_query = "INSERT INTO sapa (fullname, email, table_number, score) VALUES (%s, %s, %s, %s)"
                insert_params = (row['fullname'], row['email'], row['table_number'], row['score'])
                db_connect.execute_set_sql_query(insert_sapa_query, insert_params)

                # Обновляем или вставляем данные в sapa_bonus
                check_user_query = "SELECT bonus_score FROM sapa_bonus WHERE email = %s"
                result = db_connect.execute_get_sql_query(check_user_query, (row['email'],))

                if result:
                    # Если пользователь уже существует, пересчитаем total_score
                    current_bonus_score = result[0][0]  # Используем числовой индекс [0][0]
                    new_total_score = current_bonus_score + row['score']
                    update_total_score_query = """
                        UPDATE sapa_bonus 
                        SET total_score = %s
                        WHERE email = %s
                    """
                    db_connect.execute_set_sql_query(update_total_score_query, (new_total_score, row['email']))
                else:
                    # Если пользователь не существует, добавим его с начальным значением bonus_score = 0
                    insert_user_query = """
                        INSERT INTO sapa_bonus (email, bonus_score, total_score)
                        VALUES (%s, %s, %s)
                    """
                    insert_params = (row['email'], 0, row['score'])
                    db_connect.execute_set_sql_query(insert_user_query, insert_params)

            bot.send_message(user_id, "Кесте сәтті жаңартылды!")
            msg = bot.send_message(user_id, "Төменде қол жетімді опциялардың бірін таңдаңыз:")
            bot.register_next_step_handler(msg, sapa_instruments, bot)
        except Exception as e:
            bot.send_message(user_id, f"Кестені жүктеу кезінде қате: {e}")
    else:
        bot.send_message(user_id, "Файлды Excel форматында жүктеңіз.")
        msg = bot.send_message(user_id, "Төменде қол жетімді опциялардың бірін таңдаңыз:")
        bot.register_next_step_handler(msg, sapa_instruments, bot)
        '''

def hse_competition_(bot, message, id_i_s = None):
    text = "Сақталған ақпарат\n\n"
    full_name = "Аты-жөні: " + str(get_lastname(message)) + " " + get_firstname(message) + "\n"
    branch = "Дивизион: " + str(get_branch(message.chat.id)) + "\n"
    phone_num = "Телефон нөмірі: " + str(get_phone_number(message)) + "\n"
    text = text + full_name + branch + phone_num + ("\n\nЕгер ақпарат дұрыс сақталмаса, "
                                                    "сіз /menu түймесін басып, 'менің профиль' өту арқылы өзгерте аласыз")
    bot.send_message(message.chat.id, text)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup = generate_buttons(hse_com_field, markup)
    msg = bot.send_message(message.chat.id, "Сіз қандай байқауға қатысқыңыз келеді?", reply_markup=markup)

    if redirect(bot, message, id_i_s):
        return
    else:
        bot.register_next_step_handler(msg, hse_get_competition_name_kaz, bot)


def hse_get_competition_name_kaz(message, bot, id_i_s = None):
    if redirect(bot, message, id_i_s):
        return
    else:
        hse_competition.insert_into_hse_competition(message.chat.id)
        hse_competition.set_competition(message.chat.id, message.text)
        msg = bot.send_message(message.chat.id, "Лауазымынызды еңгізіңіз")
        bot.register_next_step_handler(msg, hse_get_position_kaz, bot)


def hse_get_position_kaz(message, bot, id_i_s = None):
    if redirect(bot, message, id_i_s):
        return
    else:
        hse_competition.set_position(message.chat.id, message.text)
        msg = bot.send_message(message.chat.id, "Сіз қай қаладансыз?")
        bot.register_next_step_handler(msg, hse_get_city_kaz, bot)

def hse_get_city_kaz(message, bot, id_i_s = None):
    if redirect(bot, message, id_i_s):
        return
    else:
        user_id = message.chat.id
        # Обновляем город пользователя
        hse_competition.set_city(user_id, message.text)

        # Сохраняем текущее время
        current_time = datetime.now()  # Получаем текущее время
        hse_competition.set_time(user_id, current_time)  # Записываем время в базу
        bot.send_message(message.chat.id, "Сіз тіркеуді аяқтадыңыз ")
        menu(bot, message)

def marathon(bot, message):
    bot.send_message(message.chat.id, "Цифрлық марафонға қатысу үшін қосымша ақпарат")
    if not maraphonersClass.ifExistsUser(message.chat.id):
        maraphonersClass.insert_into_maraphoners(message)
    msg = bot.send_message(message.chat.id, "Лауазымыңызды жазыңыз")
    bot.register_next_step_handler(msg, change_position_kaz, bot)


def change_position_kaz(message_, bot):
    if check_is_command(bot, message_, message_.text):
        return
    maraphonersClass.set_position(message_, message_.text)
    msg = bot.send_message(message_.chat.id, "Жасыңызды енгізіңіз")
    bot.register_next_step_handler(msg, change_age_kaz, bot)


def change_age_kaz(message_, bot):
    if check_is_command(bot, message_, message_.text):
        return
    try:
        age = int(message_.text)
        if age < 5 or age > 100:
            raise ValueError("Возраст вне допустимого диапазона")
    except ValueError:
        msg = bot.send_message(message_.chat.id, "Жасыңызды енгізіңіз")
        bot.register_next_step_handler(msg, change_age_kaz, bot)
        return
    maraphonersClass.set_age(message_, message_.text)
    markup_ = types.ReplyKeyboardMarkup()
    markup_ = generate_buttons(regions_, markup_)
    msg = bot.send_message(message_.chat.id, "Аймағыңызды таңдаңыз", reply_markup=markup_)
    bot.register_next_step_handler(msg, change_region_kaz, bot)


def change_region_kaz(message_, bot):
    if check_is_command(bot, message_, message_.text):
        return
    if message_.text not in regions_:
        markup_ = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_ = generate_buttons(regions_, markup_)
        msg = bot.send_message(message_.chat.id, "Тізімнен аймағыңызды таңдау керек", reply_markup=markup_)
        bot.register_next_step_handler(msg, change_region_kaz, bot)
        return
    maraphonersClass.set_region(message_, message_.text)
    formatted_number = str(maraphonersClass.get_id(message_)).zfill(4)

    bot.send_message(message_.chat.id, "Тіркеу заңды!\nВаш тіркеу нөмірі\n<b>"+formatted_number+" </b>")
    bot.send_message(message_.chat.id, str(marathoner_text_kaz(message_.chat.id)) +
                     "\nЕгер сіз өз деректеріңізді дұрыс көрсетпегендей сезінсеңіз, "
                     "онда сіз негізгі мәзірге өтіп, сандық марафонға қайта тіркеле аласыз")
    bot.send_message(message_.chat.id, "Ресми сайтқа өту үшін сілтемеге өтіңіз"
                                       "жеделхат-марафон арнасы (барлық ақпарат сол жерге жіберіледі). "
                                       "\nСілтеме: https://t.me/+edydGmWNMh43Zjcy")


def marathoner_text_kaz(user_id):
    marathoner_info = maraphonersClass.get_by_user_id(user_id)[0]
    text = f"ФИО: {marathoner_info[2]} {marathoner_info[3]}\n" \
           f"Телефон нөмірі: {marathoner_info[4]}\n" \
           f"Филиалы: {marathoner_info[5]}\n" \
           f"Лауазымы: {marathoner_info[7]}\n" \
           f"Аймақ: {str(marathoner_info[8])}\n" \
           f"Жасы: {str(marathoner_info[6])}\n"
    return text

def start_adaption(bot, message):
    markup_adapt = types.InlineKeyboardMarkup()
    button_adapt = types.InlineKeyboardButton('Айтыңызшы!', callback_data='Айтыңызшы!')
    markup_adapt.add(button_adapt)
    bot.send_message(message.chat.id, f'"Қазақтелеком" АҚ - ға қош келдіңіз🥳')
    send_photo_(bot, message.chat.id, 'images/dear_collegue_kaz.jpg')
    time.sleep(0.75)
    bot.send_message(message.chat.id, 'Бастау үшін сізге мені қалай пайдалану керектігін айтамын 🫡',
                     reply_markup=markup_adapt)


def adaption(bot, message):
    if message.text == '😊Welcome курс | Бейімделу':
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


def performer_text(appeal_info, message):
    status = kaz_get_status(message, appeal_info[0])
    performer_info = get_performer_by_category(category=appeal_info[3])
    category = rename_category_to_kaz(categories_, appeal_info[3])
    text = f"<b>ID</b> {appeal_info[0]}\n\n" \
           f" Мәртебесі: {status}\n" \
           f" Құрылған күні: {str(appeal_info[5])}\n" \
           f" Санат: {category}\n" \
           f" Мәтін: {str(appeal_info[4])}\n" \
           f" Соңғы мәртебе өзгерген күн: {str(appeal_info[6])}\n\n" \
           f"Орындаушы\n" \
           f" ТАӘ: {performer_info[4]} {performer_info[3]}\n" \
           f" Телефон нөмірі: {performer_info[5]}\n" \
           f" Email: {performer_info[6]}\n" \
           f" Telegram: {performer_info[7]}\n\n" \
           f" Пікір: {str(appeal_info[8])}"
    return text

def kaz_get_status(message, appeal_id):
    language = userClass.get_language(message)
    status = get_status(appeal_id)[0][0]
    if language == "kaz":
        if status == "Решено":
            return "Шешілді"
        elif status == "В процессе":
            return "Процесінде"
        return "Өтініш қабылданды"
    return status

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
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=None)
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
                                     f"Сілтеме мақұлданды. Қатысушыға '{link_type}' түрі үшін {new_bonus_score} ұпайлары берілді!")

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
                                f"Сіздің сілтемеңіз тексерілді.\n"
                                f"Осы сілтеме үшін бонустық ұпайлар: {bonus_score}\n"
                                f"Жалпы есеп: {total_score}"
                            )
                            bot.send_message(user_chat_id, message)
                            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                            markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'),
                                       types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

                            msg = bot.send_message(user_id, "Әрекеттердің бірін таңдаңыз:", reply_markup=markup)
                            bot.register_next_step_handler(msg, sapa_main_menu, bot)
                        else:
                            bot.send_message(user_chat_id, "Бонустық ұпайлар мен жалпы шот табылған жоқ.")
                            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                            markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'),
                                       types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

                            msg = bot.send_message(user_id, "Әрекеттердің бірін таңдаңыз:", reply_markup=markup)
                            bot.register_next_step_handler(msg, sapa_main_menu, bot)
                    else:
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'),
                                   types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

                        msg = bot.send_message(user_id, "Әрекеттердің бірін таңдаңыз:", reply_markup=markup)
                        bot.register_next_step_handler(msg, sapa_main_menu, bot)
                else:
                    bot.send_message(call.message.chat.id, "Қате: сілтеме табылмады.")
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                    markup.add(types.KeyboardButton('Sapa+ бонустық жүйесі'),
                               types.KeyboardButton('Нұсқаулар, техникалық қолдау және табыстау нүктелері'))

                    msg = bot.send_message(user_id, "Әрекеттердің бірін таңдаңыз:", reply_markup=markup)
                    bot.register_next_step_handler(msg, sapa_main_menu, bot)
            else:
                bot.send_message(call.message.chat.id,
                                 "Қате жауап. Сілтеме түрін таңдап, сілтеме нөмірін көрсетіңіз.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Әкімшінің жауабын өңдеу кезінде қате: {e}")

    if call.data == 'Начинаем!':
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
                                               'Все документы вы можете найти в разделе "ДТК Инструкции"', reply_markup=markup_callback)
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
    elif call.data == 'Айтыңызшы!':
        cm_sv_db(call.message, 'Айтыңызшы!')
        send_photo_(bot, call.message.chat.id, 'images/picture kaz.jpg')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Түсінікті", callback_data="Түсінікті")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Менде пернетақта бар⌨️, оның көмегімен сіз бөлімдерге өтіп, өзіңізге "
                                               "қажетті ақпаратты ала аласыз",
                         reply_markup=markup_callback)
    elif call.data == "Түсінікті":
        bot.send_photo(call.message.chat.id, photo=open('images/hello kaz.jpg', 'rb'))
        send_photo_(bot, call.message.chat.id, 'images/picture.jpg')

        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Кеттік!", callback_data="Кеттік!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Төмендегі түймешікті басыңыз👇🏻, жалғастырамыз.",
                         reply_markup=markup_callback)
    elif call.data == "Кеттік!":
        bot.send_photo(call.message.chat.id, photo=open('images/kaztelecom_credo_kaz.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "'Қазақтелеком' АҚ - Қазақстан Республикасы Министрлер Кабинетінің "
                                               "1994 жылғы 17 маусымдағы қаулысына сәйкес құрылған, Қазақстанның ірі "
                                               "телекоммуникациялық компаниясы.📌Бізде сізге арнайы дайындалған "
                                               "Компанияның қысқаша тарихы бар. Төмендегі файлдарды ашып, онымен "
                                               "танысыңыз.")
        bot.send_document(call.message.chat.id, open('images/Наша история 1.jpg', 'rb'))
        bot.send_document(call.message.chat.id, open('images/Наша история 2.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Кеттік!", callback_data="Ал, Кеттік!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Егер бәрі түсінікті болса, біз жалғастырамыз ба?",
                         reply_markup=markup_callback)
    elif call.data == "Ал, Кеттік!":
        bot.send_message(call.message.chat.id, "Сізде Бадди бар ма?😁")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Егер жоқ болса, көңіліңізді түсірмеңіз, ол сізді жақын арада табады!")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Ия, көбірек білгім келеді!", callback_data="Ия, көбірек білгім келеді!")
        markup.add(button)
        bot.send_message(call.message.chat.id,
                         "Сізде бұл кім және маған не үшін қажет деген сұрақ туындаса, мен жауап беремін",
                         reply_markup=markup)
    elif call.data == "Ия, көбірек білгім келеді!":
        bot.send_photo(call.message.chat.id, photo=open('images/buddy kaz - 1.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_photo(call.message.chat.id, photo=open('images/buddy kaz - 2.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Сонымен, корпоративтік e-mail-ді тексеріңіз, сізге Баддиден біздің Компаниядағы бейімделу "
                         "бағдарламасымен танысу туралы хабарлама келген шығар. ")
        time.sleep(0.75)
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Қабылданды!", callback_data="Қабылданды!")
        markup.add(button)
        bot.send_photo(call.message.chat.id, photo=open('images/buddy kaz - 3.jpg', 'rb'), reply_markup=markup)
    elif call.data == "Қабылданды!":
        bot.send_message(call.message.chat.id,
                         "Әдетте қолдау бір айға созылып, көбіне сынақ мерзімі сәтті аяқталғанға дейін жалғасады.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Айтпақшы, кез-келген бөлімнің жұмыскері Бадди бағдарламасына қатыса алады және бұл өте "
                         "жақсы-көлденең және тік байланыстар кеңейеді.")
        time.sleep(0.75)
        markup_1 = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton("Керемет, әрі қарай жалғастырамыз!",
                                              callback_data="Керемет, әрі қарай жалғастырамыз!")
        markup_1.add(button_1)
        bot.send_message(call.message.chat.id,
                         text="Болашақта жаңадан келгендерге бейімделуге көмектесіп, сіз де Бадди бола аласыз!  😊",
                         reply_markup=markup_1)
    elif call.data == "Керемет, әрі қарай жалғастырамыз!":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-1")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/credo_1_kaz.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Келесі-1":
        bot.send_message(call.message.chat.id,
                         "Біздің компания 9 филиалдан тұрады және олардың аббревиатураларын күн сайын жұмыста міндетті"
                         " түрде естисіз.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сол себепті Компанияның құрылымымен танысайық.")
        time.sleep(0.75)
        bot.send_document(call.message.chat.id, open('images/struct.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Сізге бейтаныс терминдер немесе аббревиатуралар кездессе, онда біз сізге білім қорында "
                         "глоссарий дайындадық.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Сіз әрқашан негізгі мәзірден білім қорын таба аласыз.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-3")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/gloss.jpg', 'rb'), reply_markup=markup_callback)
    elif call.data == "Келесі-3":
        bot.send_message(call.message.chat.id, '"Қазақтелеком" АҚ-да түрлі бағыттар бойынша өнімдер бар:\
                                             \n🌍Ғаламтор \n📞Телефон\n📹Бейнебақылау\n🖥️TV+ \n🛍️Дүкен shop.telecom.kz')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-4")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id,
                         "Өнімдер мен олардың тарифтері туралы өзекті ақпаратты сіз әрқашан сайттан таба аласыз "
                         "telecom.kz",
                         reply_markup=markup_callback)
    elif call.data == "Келесі-4":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-5")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/dear_users_kaz.jpg', 'rb'),
                       reply_markup=markup_callback)
    elif call.data == "Келесі-5":
        bot.send_message(call.message.chat.id,
                         '☎️" Қазақтелеком " АҚ-да "Нысана" жедел желісі біріктірілген, онда әр жұмыскер QR-код арқылы '
                         'немесе төмендегі суретте көрсетілген байланыс нөміріне хабарласа алады. ')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Келесі", callback_data="Келесі-6")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/call_center_kaz.jpg', 'rb'),
                       reply_markup=markup_callback)
    elif call.data == "Келесі-6":
        bot.send_message(call.message.chat.id,
                         "Керемет! \nКомпания туралы негізгі ақпаратпен таныстыңыз. Әрқашан боттың негізгі мәзіріндегі "
                         "білім қорын немесе жиі қойылатын сұрақтар бөлімін пайдалана аласыз.Компания туралы негізгі "
                         "ақпаратпен таныстыңыз. Әрқашан боттың негізгі мәзіріндегі білім қорын немесе жиі қойылатын "
                         "сұрақтар бөлімін пайдалана аласыз.")
        time.sleep(0.75)
        markup_welcome = types.InlineKeyboardMarkup()
        button_ = types.InlineKeyboardButton("Түсінікті!", callback_data="Түсінікті!")
        markup_welcome.add(button_)
        bot.send_photo(call.message.chat.id, photo=open('images/picture kaz.jpg', 'rb'), reply_markup=markup_welcome)
    elif call.data == "Түсінікті!":
        cm_sv_db(call.message, 'Welcome курс | Бейімделу end')
        bot.send_message(call.message.chat.id,
                         "Құттықтаймыз!\nСіз Welcome курсынан өттіңіз. \n\nКомпанияға қош келдіңіз!"
                         "\nМұнда сіз сәтті жұмыс істеу үшін қажетті барлық қосымша ақпаратты таба аласыз.")
        bot.send_document(call.message.chat.id,
                          document=open("files/Қосымша 2 Қазақтелеком АҚ ға қош келдіңіз каз.pptx", 'rb'))
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
        bot.send_message(call.message.chat.id, "Негізгі мәзірге өту үшін /menu пәрменін теріңіз немесе басыңыз")
    elif call.data == "checkPoint":
        markup_p = types.InlineKeyboardMarkup()
        button_p1 = types.InlineKeyboardButton("iOS", callback_data="iOS")
        button_p2 = types.InlineKeyboardButton("Android", callback_data="Android")
        markup_p.add(button_p1, button_p2)
        bot.send_message(str(call.message.chat.id), "Санатты таңдаңыз", reply_markup=markup_p)
    elif call.data == portal_[5]:
        markup_p = types.InlineKeyboardMarkup()
        button_p1 = types.InlineKeyboardButton(text="App Store сілтемесі",
                                               url="https://apps.apple.com/ru/app/check-point-capsule-connect/"
                                                   "id506669652")
        markup_p.add(button_p1)
        bot.send_message(str(call.message.chat.id),
                         "iOS жүйесіндегі checkpoint бейне нұсқаулығына сілтеме\nhttps://youtu.be/giK26_GgVgE ",
                         reply_markup=markup_p)
    elif call.data == portal_[6]:
        markup_p = types.InlineKeyboardMarkup()
        button_p2 = types.InlineKeyboardButton(text="PlayMarket сілтемесі",
                                               url="https://play.google.com/store/apps/details?id=com.checkpoint."
                                                   "VPN&hl=en&gl=US&pli=1")
        markup_p.add(button_p2)
        bot.send_message(str(call.message.chat.id),
                         "Android жүйесіндегі checkpoint бейне нұсқаулығына сілтеме\nhttps://youtu.be/KjL9tpunb4U",
                         reply_markup=markup_p)
    elif call.data == "abbr":
        msg = bot.send_message(call.message.chat.id, "Аббревиатураны енгізіңіз")
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
        btn = types.InlineKeyboardButton('Орындаушыға жазыңыз', callback_data=str(appeal_info[0]) + 'texting')
        text = performer_text(appeal_info, message=call.message)
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
        msg = bot.send_message(call.message.chat.id, 'Түсініктеме енгізіңіз')
        bot.register_next_step_handler(msg, add_comment, bot, appeal_id, False)
    elif extract_text(call.data, r'^.*abbr_save$', 'abbr_save') is not None:
        text = extract_text(call.data, r'^.*abbr_save$', 'abbr_save')
        send_abbr(bot, call.message, text)
    elif extract_text(call.data, r'^.*abbr_add$', 'abbr_add') is not None:
        text = extract_text(call.data, r'^.*abbr_add$', 'abbr_add')
        msg = bot.send_message(call.message.chat.id, "Аббревиатураның транскрипциясын енгізіңіз")
        bot.register_next_step_handler(msg, get_decoding, bot, text)
    elif extract_number(str(call.data), r'^(\d+)add_act') is not None:
        set_appeal_field(call.message, True)
        bot.send_message(call.message.chat.id, "Отправьте фотографию акта")
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
        text = performer_text(appeal_info, message=call.message)
        bot.send_message(appeal_info[1], "Мәртебесі өзгертілді")
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
            bot.send_message(appeal_info[1], "Шешілген үндеуді 1-ден 5-ке дейін бағалаңыз\n\nҚайда 1-өте нашар, "
                                             "5-керемет", reply_markup=markup_callback)
    elif extract_numbers_from_status_change_decided(str(call.data)) is not None:
        evaluation, appeal_id = extract_numbers_from_status_change_decided(str(call.data))
        set_evaluation(appeal_id, evaluation)
        bot.edit_message_text("Пікіріңіз үшін рахмет.\nСіз бізге жақсы адам болуға көмектесесіз", call.message.chat.id,
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
    button1 = types.InlineKeyboardButton("Аббревиатураны жіберу", callback_data=message.text + "abbr_save")
    button2 = types.InlineKeyboardButton("Транскрипт қосу", callback_data=message.text + "abbr_add")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Келесі қадамды таңдаңыз", reply_markup=markup)


def send_abbr(bot, message, text):
    bot.send_message(message.chat.id, "Аббревиатура сақталды, көмек үшін рахмет")
    bot.send_message('6682886650', "Предложение добавления глоссария\n" + text)


def get_decoding(message, bot, text):
    send_abbr(bot, message, text + " - " + message.text)


def add_comment(message, bot, appeal_id, isAdmin=True):
    comment_ = '\n' + "Пользователь: "
    if isAdmin:
        comment_ = '\n' + "Исполнитель: "
    comment = str(get_comment(appeal_id)[0][0]) + comment_ + message.text
    set_comment(appeal_id, comment)
    appeal_info = get_appeal_by_id(appeal_id)[0]
    image_data = get_image_data(appeal_id)
    text = performer_text(appeal_info, message)
    performer_id = performerClass.get_performer_id_by_id(appeal_info[7])
    try:
        bot.send_photo(appeal_info[1], image_data)
    except:
        print("error")

    if isAdmin:
        bot.send_message(appeal_info[1], text)
        bot.send_message(message.chat.id, "Түсініктеме қосылды")
    else:
        bot.send_message(performer_id, text)
        bot.send_message(message.chat.id, "Түсініктеме қосылды")


def appeal(bot, message, message_text):
    set_appeal_field(message, True)
    if message_text == "Менің өтініштерім":
        markup_a = appeal_inline_markup(message, "kaz", categories_)
        if markup_a.keyboard:
            bot.send_message(message.chat.id, "Мұнда сіз өтініштеріңіздің күйін бақылай аласыз",
                             reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, "Бұл жерде әлі бос,\nбірақ сіз апелляцияны қалдыра аласыз және ол "
                                              "осы жерде көрсетіледі")
    elif message_text == "Өтінішті қалдыру" or message_text == portal_bts[2]:
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button2_ap = types.KeyboardButton("Иә")
        markup_ap.add(button2_ap)
        profile(bot, message)
        bot.send_message(message.chat.id, "Ақпарат дұрыс па?", reply_markup=markup_ap)
    elif message_text == "Иә":
        if get_category_users_info(message) == 'Портал "Бірлік"':
            appeal(bot, message, "portal")
            return
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_ap.add(types.KeyboardButton("EX-ке сұрақ"))
        markup_ap = generate_buttons(categories_[:4], markup_ap)
        markup_ap.add(types.KeyboardButton("Сатып алу қызметі"))
        bot.send_message(message.chat.id, "Өтініш санатын таңдаңыз", reply_markup=markup_ap)
    elif message_text == "portal":
        bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')
    elif message_text == "Сатып алу қызметі":
        markup_a = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup_a = generate_buttons(categories_[4:], markup_a)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_a)
    elif message_text == "EX-ке сұрақ":
        branch = get_branch(message.chat.id)
        set_category(message, "Вопрос к EX")
        if branch == 'Обьединение Дивизион "Сеть"':
            markup_a = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup_a = generate_buttons(get_subsubcategories_by_subcategory('Обьединение Дивизион "Сеть"'), markup_a)
            bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_a)
        else:
            bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')
    elif message_text in list_categories() or message_text in categories_ \
            or message_text in get_categories_by_parentcategory("Закупочная деятельность"):
        category = rename_category_to_rus(categories_, message.text)
        set_category(message, category)
        bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')
    elif message_text == "Фотосурет қосыңыз":
        bot.send_message(message.chat.id, "Фотосуретті жіберіңіз")
    elif message_text in get_subsubcategories_by_subcategory('Обьединение Дивизион "Сеть"'):
        set_subsubcategory_users_info(message.chat.id, message_text)
        bot.send_message(message.chat.id, 'Өтінішіңізді сипаттаңыз:')
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
    elif message_text == "Фотосуретсіз жіберу":
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
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1_ap = types.KeyboardButton("Фотосурет қосыңыз")
        button2_ap = types.KeyboardButton("Фотосуретсіз жіберу")
        markup_ap.add(button2_ap, button1_ap)
        bot.send_message(message.chat.id, "Сіз фотосуретті апелляциямен бірге жібере аласыз", reply_markup=markup_ap)
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
    bot.send_message(message.chat.id, "Сіздің өтінішіңіз қабылданды")
    clear_appeals(message)
    menu(bot, message)


def end_appeal_gmail(bot, message, appeal_id, file=None):
    appeal_ = get_appeal_by_id(appeal_id)[0]
    text = get_user_info(message.chat.id)
    appeal_text = f'{text} \n {get_appeal_text(appeal_id)}'
    send_gmails(appeal_text, appeal_[3], file)
    bot.send_message(str(message.chat.id), "Сіздің өтінішіңіз сәтті жіберілді")


def faq(bot, message):
    if message.text == "Жиі қойылатын сұрақтар":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button_d = types.KeyboardButton("Демеу")
        button_hr = types.KeyboardButton("HR сұрақтары")
        button_1 = types.KeyboardButton("Қарыздар бойынша сұрақтар")
        button_p1 = types.KeyboardButton("Сатып алу қызметі бойынша сұрақтар")
        button_p2 = types.KeyboardButton("Сатып алу порталы бойынша сұрақтар")
        markup_faq.add(button_d, button_hr, button_1, button_p1, button_p2)
        bot.send_message(message.chat.id, "Мұнда сіз жиі қойылатын сұрақтарға жауап таба аласыз",
                         reply_markup=markup_faq)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер жаңа бөлім немесе сұрақтарға жауап қосу бойынша ұсыныстар/идеялар болса, бізге жазыңыз "
                         "info.ktcu@telecom.kz - Біз сіздің ұсынысыңызды міндетті түрде қарастырамыз және "
                         "сізбен байланысамыз.")
    elif message.text == "Демеу":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_1:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
    elif message.text == "HR сұрақтары":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_2:
            button_hr = types.KeyboardButton(key)
            markup_faq.add(button_hr)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
    elif message.text == "Қарыздар бойынша сұрақтар":
        branch = get_branch(message.chat.id)
        if branch == "Центральный Аппарат":
            markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
            markup_faq = generate_buttons(branches[1:], markup_faq)
            bot.send_message(message.chat.id, "Филиалды таңдаңыз", reply_markup=markup_faq)
        elif branch in branches[1:]:
            bot.send_message(message.chat.id, f"Филиал {branch}\n\n"
                                              "Қарыздар бойынша сұрақтарды келесі байланыс нөміріне жіберуге болады")
            func_branch(bot, message, branch)
    elif message.text == "Сатып алу қызметі бойынша сұрақтар":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_procurement_activities:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
    elif message.text == "Сатып алу порталы бойынша сұрақтар":
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_procurement_portal:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Сұрақты таңдаңыз", reply_markup=markup_faq)
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
    if message.text == "👷ҚТ ж ЕҚ кәртішкесін толтыру":
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button = types.KeyboardButton("Қауіпті фактор | шарт")
        button2 = types.KeyboardButton("Жұмысты орындау тәртібі")
        button3 = types.KeyboardButton("Ұсыныстар | Идеялар")
        markup.add(button, button2, button3)
        bot.send_message(message.chat.id, "Сіз қауіпті факторды, қауіпті мінез-құлықты байқадыңыз ба немесе жұмыс "
                                          "орнындағы қауіпсіздік пен еңбекті қорғауды жақсарту бойынша ұсыныстарыңыз/"
                                          "идеяларыңыз бар ма?",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Қажетті оқиғаны таңдап, ҚТ ж ЕҚ кәртішкесін толтырыңыз.")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының сол жағында")
    elif message.text == "Қауіпті фактор | шарт":
        bot.send_message(message.chat.id,
                         "Егер Сіз жұмыс барысында қауіпті факторды немесе жағдайды байқасаңыз, төмендегі сілтемеге "
                         "өтіп, сауалнаманы толтырыңыз:"
                         "\nhttps://docs.google.com/forms/d/1eizZuYiPEHYZ8A9-TQTvhQAHJHVtmJ0H90gxUsn5Ows/edit")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол "
                         "жағындағы командалар мәзірінен.")
    elif message.text == "Жұмысты орындау тәртібі":
        bot.send_message(message.chat.id, "Егер Сіз жұмыстарды орындау кезінде мінез-құлық тәуекелдерін байқасаңыз, "
                                          "төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:\
                        \nhttps://docs.google.com/forms/d/e/1FAIpQLSftmGKV1hjBiMcwqKW1yIM83PIP2eOPqU4afa8x9z3-VeHZKA/"
                                          "viewform?usp=sf_link")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз "
                         "/menu енгізу жолағының сол жағындағы командалар мәзірінен.")
    elif message.text == "Ұсыныстар | Идеялар":
        bot.send_message(message.chat.id,
                         "Егер Сізде ұсыныстар немесе идеялар болса, төмендегі сілтемеге өтіп, сауалнаманы толтырыңыз:"
                         "\nhttps://docs.google.com/forms/d/e/"
                         "1FAIpQLSdzvAVfVH2dhFyXceKTyhZhBx9TplXUp53uLTSNzw8FejpNoA/viewform")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Егер сіз артқа оралғыңыз келсе, теріңіз /menu немесе таңдаңыз /menu енгізу жолағының сол "
                         "жағындағы командалар мәзірінен.")


def instructions(bot, message):
    if message.text == "Логотиптер және Брендбук":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Қазақтелеком АҚ")
        button2_i = types.KeyboardButton("Корпоративтік Университет")
        markup_instr.add(button1_i, button2_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Модемдер | Теңшеу":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("ADSL модемі")
        button2_i = types.KeyboardButton("IDTV консолі")
        button3_i = types.KeyboardButton("ONT модемдері")
        button4_i = types.KeyboardButton("Router 4G and Router Ethernet")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Lotus | Нұсқаулар":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Филиал серверлері бойынша деректер")
        button2_i = types.KeyboardButton("Lotus Орнату нұсқаулары")
        button3_i = types.KeyboardButton("Lotus орнату файлы")
        markup_instr.add(button1_i, button2_i, button3_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Checkpoint VPN | Қашықтан жұмыс":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("CheckPoint Орнату нұсқаулығы")
        button2_i = types.KeyboardButton("Checkpoint орнату файлы")
        markup_instr.add(button1_i, button2_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Жеке кабинет telecom.kz":
        markup_instr = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_i = types.KeyboardButton("Қызметті қалай төлеуге болады")
        button2_i = types.KeyboardButton("Төлем туралы мәліметтерді қалай көруге болады")
        button3_i = types.KeyboardButton("Қосылған қызметтерді қалай көруге болады")
        button4_i = types.KeyboardButton("'Менің Қызметтерім' Бөлімі")
        markup_instr.add(button1_i, button2_i, button3_i, button4_i)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_instr)
    elif message.text == "Iссапар | Рәсімдеу тәртібі":
        bot.send_document(message.chat.id, document=open("files/Порядок оформления командировки.pdf", 'rb'))
    elif message.text == "Филиал серверлері бойынша деректер":
        bot.send_document(message.chat.id, document=open("files/Данные по всем lotus серверам.xlsx", 'rb'))
    elif message.text == "Lotus Орнату нұсқаулары":
        bot.send_document(message.chat.id, document=open("files/Инструкция по Lotus Notes на домашнем пк_.docx", 'rb'))
    elif message.text == "Lotus орнату файлы":
        bot.send_message(message.chat.id,
                         "Установочный файл Lotus Notes: "
                         "\nhttps://drive.google.com/drive/folders/1MrpjeXavmRnUMvYUiTcylhxAIEA6dvBb?usp=drive_link")
    elif message.text == "CheckPoint Орнату нұсқаулығы":
        bot.send_document(message.chat.id, document=open("files/Инструкция по установке CheckPoint.pdf", 'rb'))
    elif message.text == "Checkpoint орнату файлы":
        bot.send_document(message.chat.id, document=open("files/E85.40_CheckPointVPN.msi", 'rb'))
    elif message.text == "Қазақтелеком АҚ":
        bot.send_message(message.chat.id,
                         "'Қазақтелеком' АҚ логотиптерімен және брендбукімен қайдан танысуға болады\n"
                         "https://drive.google.com/drive/folders/1TJOkjRhZcNauln1EFqIN6sh_D78TXvF7?usp=drive_link")
    elif message.text == "Корпоративтік Университет":
        bot.send_message(message.chat.id,
                         "Мұнда сіз Корпоративтік университеттің логотиптері мен брендбуктерін таба аласыз"
                         "\nhttps://drive.google.com/drive/folders/10JQcSDebbsBFrVPjcxAlWGXLdbn937MX?usp=sharing")
    elif message.text == "Қызметті қалай төлеуге болады":
        bot.send_document(message.chat.id, document=open("files/Как оплатить услуги Казахтелеком.pdf", 'rb'))
    elif message.text == "Төлем мәліметтерін қалай көруге болады":
        bot.send_document(message.chat.id,
                          document=open("files/Как посмотреть информацию о деталях оплаты.pdf", 'rb'))
    elif message.text == "Қосылған қызметтерді қалай көруге болады":
        bot.send_document(message.chat.id, document=open("files/Как посмотреть мои подключенные услуги.pdf", 'rb'))
    elif message.text == "Менің Қызметтерім 'Бөлімі'":
        bot.send_document(message.chat.id, document=open("files/раздел «МОИ УСЛУГИ».pdf", 'rb'))
    elif message.text == "ADSL модемі":
        bot.send_message(message.chat.id,
                         "'ADSL модемі' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\n"
                         "https://drive.google.com/drive/folders/1ZMcd4cVuX8_JUJ8OoN0rYx5d5DjwlEbz?usp=drive_link")
    elif message.text == "IDTV консолі":
        bot.send_message(message.chat.id,
                         "'IDTV консолі' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\n"
                         "https://drive.google.com/drive/folders/1ZFbUrKi9QITBLkJQ93I45dxhINSsgv7H?usp=drive_link")
    elif message.text == "ONT модемдері":
        bot.send_message(message.chat.id,
                         "'ONT модемдері' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\n"
                         "https://drive.google.com/drive/folders/1IiLJ14dKF3wQhoLYb18jJMLD6BNz3K7x?usp=drive_link")
    elif message.text == "Router 4G and Router Ethernet":
        bot.send_message(message.chat.id,
                         "'Router 4G and Router Ethernet' санаты туралы ақпарат алу үшін мына сілтемеге өтіңіз\n"
                         "https://drive.google.com/drive/folders/1EkzERKwa-DTnMW86-qJGbc_YAU2k6A74?usp=drive_link")
    elif message.text == "Сатып алу порталы | Нұсқаулар":
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1_kb = types.KeyboardButton("Бастамашылар | Нұсқаулар үшін")
        button2_kb = types.KeyboardButton("Хатшылар үшін | Нұсқаулар")
        markup_kb.add(button1_kb, button2_kb)
        bot.send_message(message.chat.id, "Нұсқаулықты таңдаңыз", reply_markup=markup_kb)
    elif message.text == "Бастамашылар | Нұсқаулар үшін":
        bot.send_message(message.chat.id, "https://youtu.be/RsNAa02QO0M")
        bot.send_document(message.chat.id, open("files/Инструкция по работе в системе Портал закупок 2.0.docx", "rb"))
    elif message.text == "Хатшылар үшін | Нұсқаулар":
        bot.send_message(message.chat.id, "Хатшыларға арналған нұсқаулар"
                                          "\nhttps://disk.telecom.kz/index.php/s/kc8PfD44Qw6X8jM")
        bot.send_message(message.chat.id, "Құпия сөз:\nsF21hOvUOp")
    elif message.text == "Абоненттер үшін Wi-Fi сигналын жақсарту":
        bot.send_message(message.chat.id, "Абоненттер үшін Wi Fi сигналын жақсарту маңыздылығы мен мүмкіндіктері - \n"
                                          "https://youtu.be/wZ9Nn6bQZsI")
    elif message.text == "Маршрутизатор мен Mesh жүйесін орнату":
        bot.send_message(message.chat.id, "Маршрутизатор мен Mesh жүйесінің параметрлері туралы бейне нұсқаулық - \n"
                                          "https://youtu.be/0ue5ODjIXXU")
    elif message.text == "Желі және теледидар+":
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1_kb = types.KeyboardButton("Желіні орнату және TCP / IP")
        button2_kb = types.KeyboardButton("ТВ + Қазақтелеком орнату")
        markup_kb.add(button1_kb, button2_kb)
        bot.send_message(message.chat.id, "Нұсқаулықты таңдаңыз", reply_markup=markup_kb)
    elif message.text == "Желіні орнату және TCP / IP":
        bot.send_document(message.chat.id, open("files/Инструкция по проверке состояния сетевой карты и "
                                                "настройка свойств протокола tcpipv4.pdf", "rb"))
    elif message.text == "ТВ + Қазақтелеком орнату":
        bot.send_document(message.chat.id,
                          open("files/Инструкция по установке приложения  «ТВ+ Казахтелеком ».pdf", "rb"))
    elif message.text == "Теледидарды Wi-fi желісіне қосу":
        bot.send_document(message.chat.id, open("files/Подключение телевизора к Wi-fi сети 5 Ггц.pdf", "rb"))
    elif message.text == 'Өлшеу құралдары':
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_kb = types.KeyboardButton("Өлшеу құралдары Нұсқаулық")
        button2_kb = types.KeyboardButton("Аннотация өлшеу құралымен жұмыс істеуге арналған нұсқаулық")
        markup_kb.add(button1_kb, button2_kb)
        bot.send_message(message.chat.id, "Нұсқаулықты таңдаңыз", reply_markup=markup_kb)
    elif message.text == "Өлшеу құралдары Нұсқаулық":
        bot.send_document(message.chat.id, open("files/Измерительные приборы инструкция.pdf", "rb"))
    elif message.text == "Аннотация өлшеу құралымен жұмыс істеуге арналған нұсқаулық":
        bot.send_document(message.chat.id, open("files/Аннотация Инструкция для работы с измерительным прибором.pdf", "rb"))
    elif message.text == "Қашықтан курстарды оқуға арналған нұсқаулық":
        bot.send_document(message.chat.id,
                          open("files/Инструкция для прохождения дистанционных курсов на портале LMS - 2.jpg", "rb"))


def kb(bot, message):
    if message.text == "🗃️Білім базасы":
        set_bool(message, False, False)
        markup_kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button_kb1 = types.KeyboardButton("Нұсқаулық базасы")
        button_kb2 = types.KeyboardButton("Глоссарий")
        button_kb3 = types.KeyboardButton("Пайдалы сілтемелер")
        button_kb4 = types.KeyboardButton("Реттеуші құжаттар")
        markup_kb.add(button_kb2, button_kb1, button_kb3, button_kb4)
        bot.send_message(message.chat.id, "Мобильді білім қорына қош келдіңіз!", reply_markup=markup_kb)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Мұнда сіз қажетті нұсқауларды таба аласыз. "
                         "Сондай-ақ, біз күнделікті қолданатын негізгі терминдердің "
                         "глоссарийін табу үшін іздеу жүйесін пайдалануға болады.")
    elif message.text == "Нұсқаулық базасы":
        set_bool(message, True, False)
        markup_instr = types.ReplyKeyboardMarkup(row_width=1)
        button1_instr = types.KeyboardButton("Логотиптер және Брендбук")
        button2_instr = types.KeyboardButton("Жеке кабинет telecom.kz")
        button3_instr = types.KeyboardButton("Модемдер | Теңшеу")
        button4_instr = types.KeyboardButton("Lotus | Нұсқаулар")
        button6_instr = types.KeyboardButton("Checkpoint VPN | Қашықтан жұмыс")
        button7_instr = types.KeyboardButton("Iссапар | Рәсімдеу тәртібі")
        button8_instr = types.KeyboardButton("Сатып алу порталы | Нұсқаулар")
        button9_instr = types.KeyboardButton("Абоненттер үшін Wi-Fi сигналын жақсарту")
        button10_instr = types.KeyboardButton("Маршрутизатор мен Mesh жүйесін орнату")
        button11_kb = types.KeyboardButton("Желі және теледидар+")
        button12_kb = types.KeyboardButton("ДТК Инструкции")
        button13_kb = types.KeyboardButton("Теледидарды Wi-fi желісіне қосу")
        button14_kb = types.KeyboardButton("Өлшеу құралдары")
        button15_kb = types.KeyboardButton("Қашықтан курстарды оқуға арналған нұсқаулық")
        markup_instr.add(button4_instr, button6_instr, button1_instr, button7_instr, button2_instr, button3_instr,
                         button8_instr, button9_instr, button10_instr, button11_kb, button14_kb, button12_kb,
                         button13_kb, button15_kb)
        bot.send_message(message.chat.id, "Бұл жерде өзіңізге пайдалы нұсқаулықты таба аласыз.",
                         reply_markup=markup_instr)
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Нұсқаулықты таңдау үшін санатты, содан кейін нұсқаулықтың "
                         "өзін мәзір-пернетақтадан таңдаңыз⌨️.")
    elif message.text == "ДТК Инструкции":
        instructions_dtk(bot, message)
    elif message.text == "Глоссарий":
        set_bool(message, False, True)
        bot.send_message(message.chat.id, "'Қазақтелеком' AҚ компаниясындағы терминдер мен "
                                          "аббревиатуралардың глоссарийі.")
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Аббревиатураның немесе терминнің түсіндірмесін немесе сипаттамасын "
                                          "алу үшін сөзді теріп, ақпарат алу үшін жіберіңіз.")
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Маңызды!\nСөзді қатесіз және артық таңбаларсыз енгізіңіз. Аббревиатураларды бас әріппен "
                         "енгізу маңызды. Мысалы: ЕППК, ОДС, ДИТ.")
    elif message.text == "Пайдалы сілтемелер":
        set_bool(message, False, False)
        time.sleep(0.5)
        markup = useful_links()
        bot.send_message(message.chat.id, "Пайдалы сілтемелер", reply_markup=markup)
    elif message.text == "Реттеуші құжаттар":
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
        bot.send_message(message.chat.id, "Реттеуші құжатты таңдаңыз:", reply_markup=markup)


def menu(bot, message):
    set_bool(message, False, False)
    markup = get_markup(message)
    bot.send_message(message.chat.id, "Сіз негізгі мәзірдесіз", reply_markup=markup)


def glossary(bot, message):
    text1 = f"Сіздің сұранысыңыз бойынша келесі мән табылды:"
    text2 = ("Бізге жақсы адам болуға көмектесіңіз!\nБіз сіздің пікіріңіз бен ұсыныстарыңызды күтеміз.\n\n"
             "Сіз бізге 'хабарлама Жазу' батырмасын басу немесе хат жіберу арқылы кері байланысыңызды жібере аласыз "
             "info.ktcu@telecom.kz.")
    button_text = "Аббревиатураны жазыңыз"
    common_file.glossary(bot, message, text1, text2, button_text)


def profile(bot, message):
    markup_ap = types.InlineKeyboardMarkup(row_width=1)
    button1_ap = types.InlineKeyboardButton("Атын Өзгерту", callback_data="Изменить Имя")
    button2_ap = types.InlineKeyboardButton("Тегін өзгерту", callback_data="Изменить Фамилию")
    button3_ap = types.InlineKeyboardButton("Телефон нөмірін өзгерту", callback_data="Изменить номер телефона")
    button4_ap = types.InlineKeyboardButton("Электрондық поштаны өзгерту", callback_data="Изменить email")
    button5_ap = types.InlineKeyboardButton("Табель нөмірін өзгерту", callback_data="Изменить табельный номер")
    button6_ap = types.InlineKeyboardButton("Филиалды өзгерту", callback_data="Изменить филиал")
    markup_ap.add(button1_ap, button2_ap, button3_ap, button4_ap, button5_ap, button6_ap)
    bot.send_message(message.chat.id, f"Сақталған ақпарат\n\n"
                                      f"Аты: {get_firstname(message)}\n"
                                      f"Тегі: {get_lastname(message)}\n"
                                      f"Телефон нөмірі: {get_phone_number(message)}\n"
                                      f"Email: {get_email(message)}\n"
                                      f"Табель нөмірі: {get_table_number(message)}\n"
                                      f"Филиалы: {get_branch(message.chat.id)}",
                     reply_markup=markup_ap)


def questions(bot, message):
    button_q = types.KeyboardButton("Менің өтініштерім")
    button_q1 = types.KeyboardButton("Өтінішті қалдыру")
    button_q2 = types.KeyboardButton("Жиі қойылатын сұрақтар")
    markup_q = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup_q.add(button_q2, button_q1, button_q)
    bot.send_message(str(message.chat.id), "Бұл бөлімде сіз өзіңіздің өтінішіңізді қалдыра аласыз немесе жиі "
                                           "қойылатын сұрақтарға жауаптарды көре аласыз", reply_markup=markup_q)
    time.sleep(0.75)
    bot.send_message(message.chat.id,
                     "Егер сіз артқа қайтқыңыз келсе, /menu таңдаңыз /menu енгізу жолағының сол жағында")


def portal(bot, message):
    message_text = message.text
    if message_text == '🖥Портал "Бірлік"':
        markup_p = types.ReplyKeyboardMarkup(row_width=1)
        markup_p = generate_buttons(portal_bts, markup_p)
        bot.send_message(str(message.chat.id), "Санатты таңдаңыз", reply_markup=markup_p)
    elif message_text == portal_bts[0]:
        with open("images/Birlik_BG.jpg", 'rb') as photo_file:
            bot.send_photo(message.chat.id, photo_file)
        bot.send_message(str(message.chat.id), "'Бірлік' қызметкерінің порталы - 'Қазақтелеком' АҚ-ның әрбір қызметкері"
                                               " үшін цифрлық трансформация фокустары шеңберінде құрылған бірыңғай "
                                               "интранет жүйесі."
                                               "Порталда бар және дамитын бөлімдер:\n"
                                               "▪ Профиль\n"
                                               "▪ Жаңалықтар\n"
                                               "▪ Қауымдастықтар\n"
                                               "▪ Күнтізбе\n"
                                               "▪ Компания құрылымы және бөлімше картасы\n"
                                               "▪ Кеңейтілген іздеу\n"
                                               "▪ Іс-шаралар афишасы\n"
                                               "▪ Кеңсенің интерактивті картасы\n"
                                               "▪ Сауалнамалар мен тесттер\n"
                                               "▪ Маркет және геймификация жүйесі\n\n"
                                               "'Бірлік' қызметкер порталының артықшылықтары:\n"
                                               "- Бірыңғай ақпараттық кеңістік\n"
                                               "Қажетті ақпаратты жылдам іздеу\n"
                                               "Тиімді ынтымақтастық және топтық жұмыс\n"
                                               "Компанияның корпоративтік мәдениеті мен құндылықтарын нығайту\n"
                                               "Сыртқы модульдерді бір кеңістікке біріктіру")
    elif message_text == portal_[0]:
        markup_p = types.InlineKeyboardMarkup()
        button_p = types.InlineKeyboardButton("Checkpoint керек пе?", callback_data="checkPoint")
        markup_p.add(button_p)
        bot.send_message(str(message.chat.id),
                         "IOS және Android жүйелеріндегі қызметкер порталына қалай кіруге болады | portal.telecom.kz"
                         "\nhttps://youtu.be/WJdS1aIBe1I",
                         reply_markup=markup_p)
    # elif message_text == portal_bts[3]:
    #     markup_p = types.ReplyKeyboardMarkup(row_width=1)
    #     markup_p = db_connect.generate_buttons(portal_guide, markup_p)
    #     bot.send_message(str(message.chat.id), "Сұрақты таңдаңыз", reply_markup=markup_p)
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
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_portal)
    elif message_text == portal_[1]:
        markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1_p = types.KeyboardButton("Қалай кіруге болады")
        button2_p = types.KeyboardButton("Жеке профиль")
        button3_p = types.KeyboardButton("Порталдан ССП өту")
        markup_pk.add(button1_p, button2_p, button3_p)
        bot.send_message(message.chat.id, "Санатты таңдаңыз", reply_markup=markup_pk)
    elif message_text == portal_[2]:
        bot.send_message(message.chat.id, "Санат туралы ақпарат алу үшін 'ДК арқылы қызметкердің порталына қалай кіруге"
                                          " болады?'төмендегі сілтемеге өтіңіз \nhttps://youtu.be/vsRIDqt_-1A")
    elif message_text == portal_[3]:
        bot.send_message(message.chat.id, "Санат туралы ақпарат алу үшін 'Жеке профильді қалай толтыруға болады?'"
                                          "төмендегі сілтемеге өтіңіз \nhttps://youtu.be/V9r3ALrIQ48")
    elif message_text == portal_[4]:
        bot.send_message(message.chat.id, "Санат туралы ақпарат алу үшін 'Порталдан ССП өту'төмендегі сілтемеге өтіңіз"
                                          "\nhttps://youtu.be/wnfI4JpMvmE")
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
 - по продаже услуг и «LTE», проект открыт для всех сотрудников структурных подразделений Дивизиона по розничному бизнесу АО "Казахтелеком", исключая участников ЕМП.
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
    performer_id = get_performer_id_by_category(message.text)
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
        bot.register_next_step_handler(msg, get_pp, bot, id_i_s)
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
    text = performer_text(appeal_info, message)
    bot.send_message(appeal_info[7], "Информация по серийному номеру сим карты и модема добавлен")
    bot.send_message(appeal_info[7], text)


def add_lte_appeal(bot, message, id_i_s):
    if redirect(bot, message, id_i_s):
        return
    lte_info = db_connect.get_sale(id_i_s)
    now = datetime.now() + timedelta(hours=5)
    now_updated = remove_milliseconds(now)
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
           f"\tДействие: {lte_info[14]}\n" \
           f"\tДоставка: {lte_info[10]}"
    if lte_info[10] == "Самостоятельно":
        text += f"\n\tSimcard: {is_none(lte_info[11])}\n" \
                f"\tМодем: {is_none(lte_info[12])}"

    appeal_id = add_appeal(message.chat.id, 'Обращение принято', lte_info[13], text, now_updated,
                           now_updated,
                           lte_info[2], ' ', False, id_i_s)
    text = get_appeal_text_all(appeal_id)
    bot.send_message(lte_info[2], text)
    bot.send_message(message.chat.id, "Ваша информация сохранена")

def send_verification_code(user_id, bot, message):
    # Генерируем и сохраняем код подтверждения
    verification_code = generate_and_save_code(user_id)
    # Текст сообщения
    text = f"Сіздің растау кодыңыз: {verification_code}"
    # Отправляем письмо через уже существующую функцию send_gmails
    common_file.send_gmails_for_verif(text, user_id, None)

    # Запускаем таймер на 5 минут
    start_verification_timer(user_id, bot, message)


# Словарь для хранения последних сообщений пользователей
user_message_history = {}

# Функция для добавления сообщения в историю пользователя
def add_message_to_history(user_id, message_text):
    if user_id not in user_message_history:
        user_message_history[user_id] = []
    # Ограничиваем количество сохраненных сообщений до 4
    if len(user_message_history[user_id]) >= 4:
        user_message_history[user_id].pop(0)  # Удаляем самое старое сообщение
    user_message_history[user_id].append(message_text)

def clear_message_history(user_id):
    if user_id in user_message_history:
        del user_message_history[user_id]

# Модифицированная функция для обработки верификации
def verify_code_kaz(message, bot):
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

            # Проверяем результат работы функции
            #bot.send_message(user_id, str(check_registration_message_in_history(user_id)))

            # Проверяем, есть ли в последних сообщениях "Регистрация на обучение"
            if userClass.check_registration_message_in_history_decl_kaz(user_id) and not userClass.get_verif_decl_status(user_id):
                sql_query = "UPDATE users SET is_verified_decl = TRUE WHERE id = %s"
                params = (user_id,)
                db_connect.execute_set_sql_query(sql_query, params)
                bot.send_message(message.chat.id, "Растау сәтті аяқталды!")
                menu(bot, message)
            else:
                bot.send_message(message.chat.id, "Растау сәтті аяқталды!")
                bot.send_message(message.chat.id, "Сіз ақпаратты өзгерткіңіз келсе, онда Менің профилім қосымшасына өтіңіз")
                cm_sv_db(message, '/end_register')
                # Вызов меню перемещен сюда, так как подтверждение завершено
                menu(bot, message)

        else:
            raise ValueError("Код сәйкес келмейді")  # Исключение, если код не совпадает
    except ValueError as e:
        # Обработка ошибок при конвертации и несоответствии кода
        bot.send_message(message.chat.id, "Қате код. Қайталап көріңіз.")
        msg = bot.send_message(message.chat.id, "Кодты қайтадан енгізіңіз:")
        bot.register_next_step_handler(msg, verify_code_kaz, bot)

def is_none(line):
    if line is None:
        return " "
    return line


def redirect(bot, message, id_i_s):
    text = message.text
    if text == "/menu":
        delete_internal_sale(id_i_s)
        menu(bot, message)
        return True
    elif text == "/start":
        delete_internal_sale(id_i_s)
        send_welcome_message(bot, message)
        return True
    return False