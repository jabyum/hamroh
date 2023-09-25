from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
def main_menu_kb(check_nurse):
    kb = InlineKeyboardMarkup(row_width=1)
    about = InlineKeyboardButton(text="О проекте", callback_data="about")
    language = InlineKeyboardButton(text="Сменить язык", callback_data="change_language")
    vacancie = InlineKeyboardButton(text="Мне нужен домашний помощник", callback_data="vacancy")
    vac_base = InlineKeyboardButton(text="Посмотреть актуальные вакансии", callback_data="vac_base")
    registration = InlineKeyboardButton(text="Хочу быть в вашей базе помощников", callback_data="registration")
    delete_registration = InlineKeyboardButton(text="Удалить свою анкету", callback_data="delete_registration")
    question = InlineKeyboardButton(text="Задать вопрос", callback_data="question")
    kb.row(vacancie)
    if check_nurse == False:
        kb.add(registration)
    elif check_nurse == True:
        kb.add(delete_registration)
    kb.row(vac_base)
    kb.row(question)
    kb.row(language)
    kb.row(about)
    return kb
def language_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    rus = KeyboardButton("Русский язык")
    uzb = KeyboardButton("O'zbek tili")
    kb.add(rus, uzb)
    return kb

def main_menu_call_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    mm = InlineKeyboardButton(text="Главное меню", callback_data="main menu")
    kb.row(mm)
    return kb
def main_menu_reply_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(mm)
    return kb
def gender_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    male = KeyboardButton("Мужской")
    female = KeyboardButton("Женский")
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(male, female, mm)
    return kb
def vac_gender_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    male = KeyboardButton("Мужчина")
    female = KeyboardButton("Женщина")
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(male, female, mm)
    return kb
def num_button_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    number = KeyboardButton("Поделиться контактом", request_contact=True)
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(number, mm)
    return kb
def vac_format_kb(check_vac):
    kb = InlineKeyboardMarkup(row_width=1)
    nurse_base = InlineKeyboardButton(text="Посмотреть базу помощников", callback_data="nurse_base")
    take_vacancy = InlineKeyboardButton(text="Оставить запрос на помощника", callback_data="take_vacancy")
    delete_vacancy = InlineKeyboardButton(text="Удалить запрос на помощника", callback_data="delete_vacancy")
    mm = InlineKeyboardButton(text="Главное меню", callback_data="main menu")
    kb.row(nurse_base)
    if check_vac == False:
        kb.add(take_vacancy)
    elif check_vac == True:
        kb.add(delete_vacancy)
    kb.row(mm)
    return kb
def disease_button_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    demention = KeyboardButton("Деменция (б-нь Альцгеймера)")
    insult = KeyboardButton("Инсульт")
    onco = KeyboardButton("Онкологическое заболевание")
    another = KeyboardButton("Другое")
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(demention, insult, onco, another, mm)
    return kb
def severity_button_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    feed = KeyboardButton("0-1")
    dress = KeyboardButton("2")
    shower = KeyboardButton("3")
    wc = KeyboardButton("4")
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(feed, dress, shower, wc, mm)
    return kb
def schedule_button_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    t8 = KeyboardButton("8 часов")
    t12 = KeyboardButton("12 часов")
    t24 = KeyboardButton("24 часа")
    another = KeyboardButton("Другое время")
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(t8, t12, t24, another, mm)
    return kb
def extrawork_button_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    yes = KeyboardButton("Да, нуждаюсь")
    no = KeyboardButton("Нет, нужен только уход за человеком с деменцией")
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(yes, no, mm)
    return kb
def period_button_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    t8 = KeyboardButton("На короткий срок ( до 10 дней)")
    t12 = KeyboardButton("На средний срок ( от 11 дней до 2 месяцев)")
    t24 = KeyboardButton("На длительный срок (от 2 месяцев)")
    mm = InlineKeyboardButton(text="Главное меню")
    kb.add(t8, t12, t24, mm)
    return kb
def delete_registration_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text="Да, удалить", callback_data="yes_delete")
    no = InlineKeyboardButton(text="Нет, не удалять", callback_data="no_delete")
    kb.row(yes, no)
    return kb
def delete_vacancy_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text="Да, удалить", callback_data="yes_delete_vac")
    no = InlineKeyboardButton(text="Нет, не удалять", callback_data="no_delete_vac")
    kb.row(yes, no)
    return kb
def main_menu_kb_uz(check_nurse):
    kb = InlineKeyboardMarkup(row_width=1)
    about = InlineKeyboardButton(text="Проект хақида", callback_data="about_uz")
    language = InlineKeyboardButton(text="Тилни ўзгартириш", callback_data="change_language")
    vacancie = InlineKeyboardButton(text="Уй кўмакчиси керак", callback_data="vacancy_uz")
    vac_base = InlineKeyboardButton(text="Жорий вакансияларни кўриш", callback_data="vac_base_uz")
    registration = InlineKeyboardButton(text="Сизнинг кўмакчилар базасида бўлишни хоҳлайман", callback_data="registration_uz")
    delete_registration = InlineKeyboardButton(text="Анкетани ўчириш", callback_data="delete_registration_uz")
    question = InlineKeyboardButton(text="Савол бериш", callback_data="question_uz")
    kb.row(vacancie)
    if check_nurse == False:
        kb.add(registration)
    elif check_nurse == True:
        kb.add(delete_registration)
    kb.row(vac_base)
    kb.row(question)
    kb.row(language)
    kb.row(about)
    return kb
def main_menu_call_kb_uz():
    kb = InlineKeyboardMarkup(row_width=1)
    mm = InlineKeyboardButton(text="Бош меню", callback_data="main menu_uz")
    kb.row(mm)
    return kb
def main_menu_reply_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    mm = InlineKeyboardButton(text="Бош меню")
    kb.add(mm)
    return kb
def gender_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    male = KeyboardButton("Эркак")
    female = KeyboardButton("Аёл")
    mm = InlineKeyboardButton(text="Бош меню")
    kb.add(male, female, mm)
    return kb
def vac_gender_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    male = KeyboardButton("Эркак")
    female = KeyboardButton("Аёл")
    mm = InlineKeyboardButton(text="Бош меню")
    kb.add(male, female, mm)
    return kb
def num_button_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    number = KeyboardButton("Контакт билан улашиш", request_contact=True)
    mm = InlineKeyboardButton(text="Бош меню")
    kb.add(number, mm)
    return kb
def vac_format_kb_uz(check_vac):
    kb = InlineKeyboardMarkup(row_width=1)
    nurse_base = InlineKeyboardButton(text="Кўмакчилар базасини кўриш", callback_data="nurse_base_uz")
    take_vacancy = InlineKeyboardButton(text="Кўмакчига сўров қолдириш", callback_data="take_vacancy_uz")
    delete_vacancy = InlineKeyboardButton(text="Кўмакчига сўровни ўчириш", callback_data="delete_vacancy_uz")
    mm = InlineKeyboardButton(text="Бош меню", callback_data="main menu")
    kb.row(nurse_base)
    if check_vac == False:
        kb.add(take_vacancy)
    elif check_vac == True:
        kb.add(delete_vacancy)
    kb.row(mm)
    return kb
def disease_button_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    demention = KeyboardButton("Деменция (Альцгеймер касаллиги)")
    insult = KeyboardButton("Инсульт")
    onco = KeyboardButton("Онкологик касаллик")
    another = KeyboardButton("Бошқа")
    mm = InlineKeyboardButton(text="Бош меню")
    kb.add(demention, insult, onco, another, mm)
    return kb
def severity_button_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    feed = KeyboardButton("0-1")
    dress = KeyboardButton("2")
    shower = KeyboardButton("3")
    wc = KeyboardButton("4")
    mm = InlineKeyboardButton(text="Бош меню")
    kb.add(feed, dress, shower, wc, mm)
    return kb
def schedule_button_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    t8 = KeyboardButton("8 соат")
    t12 = KeyboardButton("12 соат")
    t24 = KeyboardButton("24 соат")
    another = KeyboardButton("Бошқа вақт")
    mm = InlineKeyboardButton(text="Бош меню")
    kb.add(t8, t12, t24, another, mm)
    return kb
def extrawork_button_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    yes = KeyboardButton("Ҳа, керак")
    no = KeyboardButton("Йўқ, фақат деменцияли одам учун парвариш керак")
    mm = InlineKeyboardButton(text="Бош меню")
    kb.add(yes, no, mm)
    return kb
def period_button_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    t8 = KeyboardButton("Қисқа муддатга ( 10 кунгача)")
    t12 = KeyboardButton("Ўртача муддатга ( 11 кундан 2 ойгача)")
    t24 = KeyboardButton("Узоқ муддатга (2 ойгача)")
    mm = InlineKeyboardButton(text="Бош меню")
    kb.add(t8, t12, t24, mm)
    return kb
def delete_registration_kb_uz():
    kb = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text="Ҳа, ўчирилсин", callback_data="yes_delete_uz")
    no = InlineKeyboardButton(text="Йўқ, ўчирилмасин", callback_data="no_delete_uz")
    kb.row(yes, no)
    return kb
def delete_vacancy_kb_uz():
    kb = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text="Ҳа, ўчирилсин", callback_data="yes_delete_vac_uz")
    no = InlineKeyboardButton(text="Йўқ, ўчирилмасин", callback_data="no_delete_vac_uz")
    kb.row(yes, no)
    return kb