import telebot
import hamrohdatabase
import hamrohbuttons
from telebot import types
import time
bot = telebot.TeleBot("6269391112:AAFlxxKYVCaFS6l2BS26nmMATi3bSCoQ1hg")
@bot.message_handler(commands=["start"])
def start_message(message):
    user_id = message.from_user.id
    mm = bot.send_message(user_id, "Главное меню", reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(user_id, mm.message_id)
    check_nurse = hamrohdatabase.check_nurse(user_id)
    bot.send_message(user_id, "Выберите действие",
                     reply_markup=hamrohbuttons.main_menu_kb(check_nurse))
@bot.callback_query_handler(lambda call: call.data in ["about", "main menu", "registration", "question",
                                                       "vacancy", "vac_base", "take_vacancy", "yes_delete",
                                                       "no_delete", "delete_registration", "delete_vacancy",
                                                       "yes_delete_vac", "no_delete_vac", "nurse_base"])
def calling(call):
    user_id = call.message.chat.id
    if call.data == "about":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Ассалому алейкум!\n\nМы рады, что вы обратились в HAMROH.\n\n"
                                  "Мы предоставляем профессиональный уход за людьми с инвалидностью на дому в Ташкенте.\n\n"
                                  "Более подробную информацию о нашей организации и услугах вы найдете на сайте hamroh.org\n\n"
                                  "Данный бот предоставляет площадку для связывания домашнего помощника с клиентом.",
                         reply_markup=hamrohbuttons.main_menu_call_kb())
    elif call.data == "main menu":
        bot.delete_message(user_id, call.message.message_id)
        return start_message(call)
    elif call.data == "delete_registration":
        bot.send_message(user_id, "Вы уверены, что хотите удалить свою анкету?",
                         reply_markup=hamrohbuttons.delete_registration_kb())
    elif call.data == "no_delete":
        bot.delete_message(user_id, call.message.message_id)
        return start_message(call)
    elif call.data == "yes_delete":
        try:
            bot.delete_message(user_id, call.message.message_id)
            nurse_message_id = hamrohdatabase.get_nurse_message_id(user_id)
            hamrohdatabase.delete_exact_nurse(user_id)
            bot.send_message(user_id, "Ваша анкета удалена")
            start_message(call)
            try:
                bot.delete_message(-1001905443362, nurse_message_id)
            except:
                pass
        except:
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Произошла ошибка. Обратиться в службу поддержки")
            return start_message(call)
    elif call.data == "delete_vacancy":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Вы уверены, что хотите удалить вакансию?",
                         reply_markup=hamrohbuttons.delete_vacancy_kb())
    elif call.data == "registration":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Для того, чтобы оставить свою анкету в базе помощников, пожалуйста ответьте"
                                  " на следующие вопросы.\n\n"
                                  "Напишите своё имя и фамилию.\n\n"
                                  "Если вы нажмете на кнопку 'Главное меню' в процессе заполнения, "
                                  "анкету придется заполнять заново",
                         reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(call.message, get_nurse_name)

    elif call.data == "question":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Напишите свой вопрос",
                         reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(call.message, take_question)
    elif call.data == "vacancy":
        bot.delete_message(user_id, call.message.message_id)
        check_vac = hamrohdatabase.check_vac(user_id)
        bot.send_message(user_id, "Вы можете выбрать и помощника из имеющихся в базе помощников "
                                  "или оставить свой запрос открытым",
                         reply_markup=hamrohbuttons.vac_format_kb(check_vac))
    elif call.data == "no_delete_vac":
        bot.delete_message(user_id, call.message.message_id)
        return start_message(call)
    elif call.data == "yes_delete_vac":
        try:
            bot.delete_message(user_id, call.message.message_id)
            vac_message_id = hamrohdatabase.get_vacancy_message_id(user_id)
            hamrohdatabase.delete_exact_vacancie(user_id)
            bot.send_message(user_id, "Ваша вакансия удалена")
            start_message(call)
            try:
                bot.delete_message(-1001925064725, vac_message_id)
            except:
                pass
        except:
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Произошла ошибка. Обратиться в службу поддержки")
            return start_message(call)
    elif call.data == "vac_base":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Канал с актуальными вакансиями\n"
                                  "https://t.me/+lyN7cNoZ40VmZDVi",
                         reply_markup=hamrohbuttons.main_menu_call_kb())
    elif call.data == "nurse_base":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Канал с анкетами сиделок\n"
                                  "https://t.me/+8BN_TP1AX8Y4ZjIy",
                         reply_markup=hamrohbuttons.main_menu_call_kb())
    elif call.data == "take_vacancy":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id,"Пожалуйста, выберите подходящий вариант. Для кого нужен помощник?\n"
                                 "Если вы нажмете на кнопку 'Главное меню' в процессе заполнения, "
                                  "анкету придется заполнять заново",
                         reply_markup=hamrohbuttons.vac_gender_kb())
        bot.register_next_step_handler(call.message, get_vac_gender)
def get_vac_gender(message):
    user_id = message.from_user.id
    sex = message.text
    if sex == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Напишите цифрами возраст человека",
                         reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_vac_age, sex)
def get_vac_age(message, sex):
    user_id = message.from_user.id
    age = message.text
    if age == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Выберите основное заболевание, из-за которого требуется помощник",
                         reply_markup=hamrohbuttons.disease_button_kb())
        bot.register_next_step_handler(message, get_vac_disease, sex, age)
def get_vac_disease(message, sex, age):
    user_id = message.from_user.id
    disease = message.text
    if disease == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Сколько из нижеследующих дел человек может самостоятельно выполнять?\n"
                                  "1.	Легкое приготовление пищи и питание\n"
                                  "2.	Одевание и раздевание\n"
                                  "3.	Купание\n"
                                  "4.	Туалет и уход за собой",
                         reply_markup=hamrohbuttons.severity_button_kb())
        bot.register_next_step_handler(message, get_vac_severity, sex, age, disease)
def get_vac_severity(message, sex, age, disease):
    user_id = message.from_user.id
    severity = message.text
    if severity == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Выберите сколько часов в день вы нуждаетесь в домашнем компаньоне?",
                         reply_markup=hamrohbuttons.schedule_button_kb())
        bot.register_next_step_handler(message, get_vac_schedule, sex, age, disease, severity)
def get_vac_schedule(message, sex, age, disease, severity):
    user_id = message.from_user.id
    schedule = message.text
    if schedule == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Нуждаетесь ли вы в дополнительной работе компаньона по домашнему хозяйству "
                                  "(уборка, стирка, готовка, совершение покупок и т.д.)",
                         reply_markup=hamrohbuttons.extrawork_button_kb())
        bot.register_next_step_handler(message, get_vac_extrawork, sex, age, disease, severity, schedule)
def get_vac_extrawork(message, sex, age, disease, severity, schedule):
    user_id = message.from_user.id
    extra_work = message.text
    if extra_work == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "На какой период вам необходим помощник?",
                         reply_markup=hamrohbuttons.period_button_kb())
        bot.register_next_step_handler(message, get_vac_period, sex, age, disease, severity, schedule, extra_work)
def get_vac_period(message, sex, age, disease, severity, schedule, extra_work):
    user_id = message.from_user.id
    period = message.text
    if period == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Отправьте ваш номер использую кнопку в меню",
                         reply_markup=hamrohbuttons.num_button_kb())
        bot.register_next_step_handler(message, get_vac_phone_number, sex, age, disease, severity, schedule, extra_work,
                                   period)

def get_vac_phone_number(message, sex, age, disease, severity, schedule, extra_work, period):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, "Напишите ниже адрес, включая название района и возможные ориентиры." 
                                  "(не отправляйте геолокацию)", reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_vac_address, sex, age, disease, severity, schedule, extra_work,
                                       period, phone_number)
    elif message.text == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку")
        bot.register_next_step_handler(message, get_vac_phone_number, sex, age, disease, severity, schedule, extra_work,
                                       period)

def get_vac_address(message,sex, age, disease, severity, schedule, extra_work, period, phone_number):
    user_id = message.from_user.id
    address = message.text
    if address == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Напишите максимальную цену, которую вы готовы заплатить за услугу помощника исходя из ответов, "
                                  "указанных вами выше?", reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_vac_salary, sex, age, disease, severity, schedule, extra_work,
                                   period, phone_number, address)
def get_vac_salary(message, sex, age, disease, severity, schedule, extra_work, period, phone_number, address):
    user_id = message.from_user.id
    salary = message.text
    if salary == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Ваш запрос отправлен", reply_markup=types.ReplyKeyboardRemove())
        posting = bot.send_message(-1001925064725, f"<b>Пол</b>: {sex}\n"
                                                   f"<b>Возраст</b>: {age}\n"
                                                   f"<b>Заболевание</b>: {disease}\n"
                                                   f"<b>Уровень самостоятельности(4-бальная шкала)</b>: {severity}\n"
                                                   f"<b>Рабочий день</b>: {schedule}\n"
                                                   f"<b>Дополнительная работа</b>: {extra_work}\n"
                                                   f"<b>Период работы</b>: {period}\n"
                                                   f"<b>Адрес</b>: {address}\n"
                                                   f"<b>Оплата</b>: {salary}\n"
                                                   f"<b>Телефон</b>: {phone_number}", parse_mode="html")
        message_id = posting.message_id
        hamrohdatabase.add_vac(user_id, sex, age, disease, severity, schedule, extra_work, period,
                               phone_number, address, salary, message_id)
        start_message(message)
def take_question(message):
    user_id = message.from_user.id
    question = message.text
    if question == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Ваш вопрос отправлен. Вам ответят в ближайшее время",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(305896408, f"Вопрос от {user_id} \n\n"
                                f"Вопрос: {question}")
        start_message(message)
def get_nurse_name(message):
    user_id = message.from_user.id
    name = message.text
    if name == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Выберите ваш пол", reply_markup=hamrohbuttons.gender_kb())
        bot.register_next_step_handler(message, get_nurse_gender, name)
def get_nurse_gender(message, name):
    user_id = message.from_user.id
    sex = message.text
    if sex == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Напишите год своего рождения", reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_nurse_age, name, sex)
def get_nurse_age(message, name, sex):
    user_id = message.from_user.id
    age = message.text
    if age == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Коротко и четко напишите о своем образовании и специальности",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_nurse_education, name, sex, age)
def get_nurse_education(message, name, sex, age):
    user_id = message.from_user.id
    education = message.text
    if education == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Коротко и четко напишите о своем опыте работы, связанным с уходом за болеющими людьми. "
                                 "Напишите сколько лет и с какими людьми вы работали. Если вы работали нескольких местах, "
                                  "вы можете разделить каждый опыт порядковым числом (1. 2. 3.)",
                         reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_nurse_experience, name, sex, age, education)
def get_nurse_experience(message, name, sex, age, education):
    user_id = message.from_user.id
    experience = message.text
    if experience == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Напишите о навыках, которыми вы обладаете, которые могут помочь при уходе на дому.",
                         reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_nurse_skills, name, sex, age, education, experience)
def get_nurse_skills(message, name, sex, age, education, experience):
    user_id = message.from_user.id
    skills = message.text
    if skills == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Напишите адрес вашего проживания, включая район (не отправляйте геолокацию)",
                         reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_nurse_address, name, sex, age, education, experience, skills)
def get_nurse_address(message, name, sex, age, education, experience, skills):
    user_id = message.from_user.id
    address = message.text
    if address == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Отправьте ваш номер использую кнопку в меню",
                         reply_markup=hamrohbuttons.num_button_kb())
        bot.register_next_step_handler(message, get_nurse_phone_number, name, sex, age, education, experience, skills, address)
def get_nurse_phone_number(message, name, sex, age, education, experience, skills, address):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, "Пожалуйста, загрузите собственную фотографию. "
                                  "Фотография должна быть хорошего качества, сделанная при хорошем освещении. "
                                  "Не забудьте улыбаться ",
                         reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_nurse_photo, name, sex, age, education, experience, skills,
                                       address, phone_number)
    elif message.text == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку")
        bot.register_next_step_handler(message, get_nurse_phone_number, name, sex, age, education,
                                       experience, skills, address)
def get_nurse_photo(message,name, sex, age, education, experience, skills, address, phone_number):
    user_id = message.from_user.id
    if message.photo:
        photo = message.photo[-1].file_id
        bot.send_message(user_id, "Ваша анкета готова",
                         reply_markup=types.ReplyKeyboardRemove())
        posting = bot.send_photo(-1001905443362, photo=photo, caption=f"{name}\n"
                                                                      f"<b>Пол</b>: {sex}\n"
                                                                      f"<b>Возраст</b>: {age}\n"
                                                                      f"<b>Образование</b>: {education}\n"
                                                                      f"<b>Опыт</b>: {experience}\n"
                                                                      f"<b>Навыки</b>: {skills}\n"
                                                                      f"<b>Адрес</b>: {address}\n"
                                                                      f"<b>Номер телефона</b>: {phone_number}",
                                 parse_mode="html")
        message_id = posting.message_id

        hamrohdatabase.add_nurse(user_id, name, sex, age, education, experience, skills, address, phone_number, photo,
                                 message_id)
        # photo = hamrohdatabase.get_nurses_photo(user_id)
        # bot.send_photo(user_id, photo=photo[0])
        start_message(message)
    elif message.text == "Главное меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Отправьте фотографию")
        bot.register_next_step_handler(message, get_nurse_phone_number, name, sex, age, education,
                                       experience, skills, address)


# open(file, 'rb')
bot.polling(non_stop=True)
