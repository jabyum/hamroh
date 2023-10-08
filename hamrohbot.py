import telebot
import hamrohdatabase
import hamrohbuttons
from telebot import types
import time
import threading
bot = telebot.TeleBot("6527744179:AAGCZ0BFwA6VXkqZ5BVDtetE4NtfL7wg7XQ")


@bot.message_handler(commands=["start"])
def start_message(message):
    user_id = message.from_user.id
    language = hamrohdatabase.check_language(user_id)
    if language == False:
        bot.send_message(user_id, "Выберите язык / Tilni tanlang", reply_markup=hamrohbuttons.language_kb())
        bot.register_next_step_handler(message, register_user)
    elif language == "rus":
        mm = bot.send_message(user_id, "Главное меню", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(user_id, mm.message_id)
        check_nurse = hamrohdatabase.check_nurse(user_id)
        bot.send_message(user_id, "Выберите действие",
                        reply_markup=hamrohbuttons.main_menu_kb(check_nurse))
    elif language == "uzb":
        mm = bot.send_message(user_id, "Бош меню", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(user_id, mm.message_id)
        check_nurse = hamrohdatabase.check_nurse(user_id)
        bot.send_message(user_id, "Ҳаракатни танланг",
                         reply_markup=hamrohbuttons.main_menu_kb_uz(check_nurse))
@bot.callback_query_handler(lambda call: call.data in ["about", "main menu", "registration", "question",
                                                       "vacancy", "vac_base", "take_vacancy", "yes_delete",
                                                       "no_delete", "delete_registration", "delete_vacancy",
                                                       "yes_delete_vac", "no_delete_vac", "nurse_base",
                                                       "about_uz", "main menu_uz", "registration_uz", "question_uz",
                                                       "vacancy_uz", "vac_base_uz", "take_vacancy_uz", "yes_delete_uz",
                                                       "no_delete_uz", "delete_registration_uz", "delete_vacancy_uz",
                                                       "yes_delete_vac_uz", "no_delete_vac_uz", "nurse_base_uz",
                                                       "change_language", "add_admin", "del_admin", "mailing",
                                                       "close", "send_message"])
def calling(call):
    user_id = call.message.chat.id
    try:
        if call.data == "about":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Ассалому алейкум!\n\nМы рады, что вы обратились в HAMROH.\n\n"
                                      "Мы предоставляем профессиональный уход за людьми с инвалидностью на дому в Ташкенте.\n\n"
                                      "Более подробную информацию о нашей организации и услугах вы найдете на сайте hamroh.org\n\n"
                                      "Данный бот предоставляет площадку для связывания домашнего помощника с клиентом.",
                             reply_markup=hamrohbuttons.main_menu_call_kb())
        elif call.data == "send_message":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Введите айди пользователя, которому вы хотите написать",
                             reply_markup=hamrohbuttons.canceling())
            bot.register_next_step_handler(call.message, send_answer)
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
                                      "https://t.me/hamrohcare_vacancy",
                             reply_markup=hamrohbuttons.main_menu_call_kb())
        elif call.data == "nurse_base":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Канал с анкетами сиделок\n"
                                      "https://t.me/hamrohcare_nurse",
                             reply_markup=hamrohbuttons.main_menu_call_kb())
        elif call.data == "take_vacancy":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id,"Пожалуйста, выберите подходящий вариант. Для кого нужен помощник?\n"
                                     "Если вы нажмете на кнопку 'Главное меню' в процессе заполнения, "
                                      "анкету придется заполнять заново",
                             reply_markup=hamrohbuttons.vac_gender_kb())
            bot.register_next_step_handler(call.message, get_vac_gender)
        elif call.data == "about_uz":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Ассалому алейкум!\n\nHAMROH га мурожаат қилганингиздан хунсандмиз.\n\n"
                                      "Тошкент шахрида ногиронлиги мавжуд одамларга профессионал парвариш хизматини таъминлаймиз.\n\n"
                                      "Бизнинг ташкилот ва хизматлар тўғрисида hamroh.org сайтидан янада батафсил маълумотни топишингиз мумкин\n\n"
                                      "Ушбу бот уй кўмакчиси ва мижоз ўртасида боғланишни таъминлайди.",
                             reply_markup=hamrohbuttons.main_menu_call_kb_uz())
        elif call.data == "main menu_uz":
            bot.delete_message(user_id, call.message.message_id)
            return start_message(call)
        elif call.data == "delete_registration_uz":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Анкетангизни ўчиришни аниқ хоҳлайсизми?",
                             reply_markup=hamrohbuttons.delete_registration_kb_uz())
        elif call.data == "no_delete_uz":
            bot.delete_message(user_id, call.message.message_id)
            return start_message(call)
        elif call.data == "yes_delete_uz":
            try:
                bot.delete_message(user_id, call.message.message_id)
                nurse_message_id = hamrohdatabase.get_nurse_message_id(user_id)
                hamrohdatabase.delete_exact_nurse(user_id)
                bot.send_message(user_id, "Сизнинг анкетангиз ўчирилди")
                start_message(call)
                try:
                    bot.delete_message(-1001905443362, nurse_message_id)
                except:
                    pass
            except:
                bot.delete_message(user_id, call.message.message_id)
                bot.send_message(user_id, "Хато юз берди. Қўллаб-қувватлаш хизматига мурожаат қилиш")
                return start_message(call)
        elif call.data == "delete_vacancy_uz":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Вакансияни ўчиришни аниқ хоғлайсизми?",
                             reply_markup=hamrohbuttons.delete_vacancy_kb_uz())
        elif call.data == "registration_uz":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Кўмакчилар базасида ўз анкетангизни қолдириш учун қуйидаги саволларга жавоб беринг.\n\n"
                                      "Ўз исм ва фамилиянгизни ёзинг.\n\n"
                                      "Тўлдириш жараёнида 'Бош меню' тугмасини боссангиз анкетани қайтадан тўлдиришга тўғри келади",
                             reply_markup=hamrohbuttons.main_menu_reply_kb_uz())
            bot.register_next_step_handler(call.message, get_nurse_name_uz)

        elif call.data == "question_uz":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Саволингизни ёзинг",
                             reply_markup=hamrohbuttons.main_menu_reply_kb_uz())
            bot.register_next_step_handler(call.message, take_question_uz)
        elif call.data == "vacancy_uz":
            bot.delete_message(user_id, call.message.message_id)
            check_vac = hamrohdatabase.check_vac(user_id)
            bot.send_message(user_id, "Кўмакчилар базасида мавжуд кўмакчини танлашингиз мумкин ёки сўровингиз очиқ қолдиришингиз мумкин",
                             reply_markup=hamrohbuttons.vac_format_kb_uz(check_vac))
        elif call.data == "no_delete_vac_uz":
            bot.delete_message(user_id, call.message.message_id)
            return start_message(call)
        elif call.data == "yes_delete_vac_uz":
            try:
                bot.delete_message(user_id, call.message.message_id)
                vac_message_id = hamrohdatabase.get_vacancy_message_id(user_id)
                hamrohdatabase.delete_exact_vacancie(user_id)
                bot.send_message(user_id, "Вакансиянгиз ўчирилди")
                start_message(call)
                try:
                    bot.delete_message(-1001925064725, vac_message_id)
                except:
                    pass
            except:
                bot.delete_message(user_id, call.message.message_id)
                bot.send_message(user_id, "Хато юз берди. Қўллаб-қувватлаш хизматига мурожаат қилиш")
                return start_message(call)
        elif call.data == "vac_base_uz":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Жорий вакансиялар канали\n"
                                      "https://t.me/+lyN7cNoZ40VmZDVi",
                             reply_markup=hamrohbuttons.main_menu_call_kb_uz())
        elif call.data == "nurse_base_uz":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Энагалар анкеталари канали\n"
                                      "https://t.me/+8BN_TP1AX8Y4ZjIy",
                             reply_markup=hamrohbuttons.main_menu_call_kb_uz())
        elif call.data == "take_vacancy_uz":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id,"Тегишли вариантни танланг. Кўмакчи ким учун керак?\n"
                                     "Тўлдириш жараёнида 'Бош меню' тугмасини боссангиз анкетани қайтадан тўлдиришга тўғри келади",
                             reply_markup=hamrohbuttons.vac_gender_kb_uz())
            bot.register_next_step_handler(call.message, get_vac_gender_uz)
        elif call.data == "change_language":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Выберите язык / Tilni tanlang", reply_markup=hamrohbuttons.language_kb())
            bot.register_next_step_handler(call.message, change_language)
        elif call.data == "add_admin":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Введите tg-id нового админа",
                             reply_markup=hamrohbuttons.canceling())
            bot.register_next_step_handler(call.message, add_admin)
        elif call.data == "close":
            bot.delete_message(user_id, call.message.message_id)
        elif call.data == "del_admin":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Введите tg id адмна",
                             reply_markup=hamrohbuttons.canceling())
            bot.register_next_step_handler(call.message, delete_admin)
        elif call.data == "mailing":
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(user_id, "Введите текст рассылки, либо отмените рассылку через кнопку в меню",
                             reply_markup=hamrohbuttons.canceling())
            bot.register_next_step_handler(call.message, mailing_to_all)
    except:
        pass

def send_answer(message):
    admin_id = message.from_user.id
    if message.text == "Отмена❌":
        bot.send_message(admin_id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            user_id = int(message.text)
            bot.send_message(admin_id, "Введите сообщения для пользователя", reply_markup=hamrohbuttons.canceling())
            bot.register_next_step_handler(message, send_full_answer, user_id)
        except:
            bot.send_message(admin_id, "Неправильный айди", reply_markup=types.ReplyKeyboardRemove())

def send_full_answer(message, user_id):
    admin_id = message.from_user.id
    text = message.text
    if message.text == "Отмена❌":
        bot.send_message(admin_id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            bot.send_message(user_id, text)
            bot.send_message(admin_id, "Ответ отправлен", reply_markup=types.ReplyKeyboardRemove())
        except:
            bot.send_message(admin_id, "Не удалось отправить ответ", reply_markup=types.ReplyKeyboardRemove())

def send_message_to_user(target_id, text):
    target = target_id[0]
    try:
        time.sleep(1)
        bot.send_message(target, text)
    except:
        pass
def mailing_to_all(message):
    user_id = message.from_user.id
    targets_id = hamrohdatabase.mailing_all()
    text = message.text
    if text == "Отмена❌":
        bot.send_message(user_id, "Рассылка отменена", reply_markup=types.ReplyKeyboardRemove())
    else:
        for target_id in targets_id:
            thread = threading.Thread(target=send_message_to_user, args=(target_id, text))
            thread.start()
    bot.send_message(user_id, "Рассылка завершена", reply_markup=types.ReplyKeyboardRemove())
    admin_panel(message)

def delete_admin(message):
    user_id = message.from_user.id
    admin_id = message.text
    if admin_id == "Отмена❌":
         bot.send_message(user_id, "Отмена", reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            checker = hamrohdatabase.check_admin(int(admin_id))
            if checker:
                hamrohdatabase.delete_admin(int(admin_id))
                bot.send_message(user_id, "Админ удалён")
                bot.send_message(int(admin_id), "Вы больше не являетесь админом")
                bot.kick_chat_member(-1001806564382, int(admin_id))
                admin_panel(message)
            else:
                bot.send_message(user_id, "Юзер не является админом")
                admin_panel(message)
        except:
            bot.send_message(user_id, "Ошибка в id")
            admin_panel(message)
def add_admin(message):
    user_id = message.from_user.id
    new_admin_id = message.text
    rank = 1
    if new_admin_id == "Отмена❌":
         bot.send_message(user_id, "Отмена", reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            checker = hamrohdatabase.check_admin(int(new_admin_id))
            if checker:
                bot.send_message(user_id, "Юзер уже является админом")
                admin_panel(message)
            else:
                hamrohdatabase.add_admin(int(new_admin_id), rank)
                bot.send_message(user_id, "Админ добавлен")
                bot.send_message(int(new_admin_id), "Вы стали админом 1 ранга\n")

                admin_panel(message)
        except:
            bot.send_message(user_id, "Ошибка в id")
            admin_panel(message)

def change_language(message):
    user_id = message.from_user.id
    if message.text == "Русский язык":
        hamrohdatabase.change_language("rus", user_id)
        mm = bot.send_message(user_id, "Главное меню", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(user_id, mm.message_id)
        check_nurse = hamrohdatabase.check_nurse(user_id)
        bot.send_message(user_id, "Выберите действие",
                         reply_markup=hamrohbuttons.main_menu_kb(check_nurse))
    elif message.text == "O'zbek tili":
        hamrohdatabase.change_language("uzb", user_id)
        mm = bot.send_message(user_id, "Бош меню", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(user_id, mm.message_id)
        check_nurse = hamrohdatabase.check_nurse(user_id)
        bot.send_message(user_id, "Ҳаракатни танланг",
                         reply_markup=hamrohbuttons.main_menu_kb_uz(check_nurse))
    else:
        bot.send_message(user_id, "Выберите язык из списка в меню / Tilni menudan tanlang",
                         reply_markup=hamrohbuttons.language_kb())
        bot.register_next_step_handler(message, register_user)
def register_user(message):
    user_id = message.from_user.id
    if message.text == "Русский язык":
        hamrohdatabase.reg_user(user_id, "rus")
        mm = bot.send_message(user_id, "Главное меню", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(user_id, mm.message_id)
        check_nurse = hamrohdatabase.check_nurse(user_id)
        bot.send_message(user_id, "Выберите действие",
                         reply_markup=hamrohbuttons.main_menu_kb(check_nurse))
    elif message.text == "O'zbek tili":
        hamrohdatabase.reg_user(user_id, "uzb")
        mm = bot.send_message(user_id, "Бош меню", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(user_id, mm.message_id)
        check_nurse = hamrohdatabase.check_nurse(user_id)
        bot.send_message(user_id, "Ҳаракатни танланг",
                         reply_markup=hamrohbuttons.main_menu_kb_uz(check_nurse))
    else:
        bot.send_message(user_id, "Выберите язык из списка в меню / Tilni menudan tanlang",
                         reply_markup=hamrohbuttons.language_kb())
        bot.register_next_step_handler(message, register_user)
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
        bot.send_message(user_id, "Выберите основное заболевание, из-за которого требуется помощник "
                                  "или напишите его сами",
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
                                  "(не отправляйте геолокацию).\n Также вы можете написать любую важную по вашему мнению "
                                  "информацию", reply_markup=hamrohbuttons.main_menu_reply_kb())
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
                                                   f"<b>Адрес и дополнительная информация</b>: {address}\n"
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
        bot.send_message(user_id, "Напишите о навыках, которыми вы обладаете, которые могут помочь при уходе на дому."
                                  "Также вы можете написать любую важную по вашему мнению информацию",
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
                                                                      f"<b>Навыки и дополнительная информация</b>: {skills}\n"
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
        bot.register_next_step_handler(message, get_nurse_photo, name, sex, age, education,
                                       experience, skills, address, phone_number)

def get_vac_gender_uz(message):
    user_id = message.from_user.id
    sex = message.text
    if sex == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Одам ёшини рақамларда ёзинг",
                         reply_markup=hamrohbuttons.main_menu_reply_kb_uz())
        bot.register_next_step_handler(message, get_vac_age_uz, sex)
def get_vac_age_uz(message, sex):
    user_id = message.from_user.id
    age = message.text
    if age == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Кўмакчига муҳтожлик туғдирган асосий касалликни танланг ёки ўзингиз ёзинг",
                         reply_markup=hamrohbuttons.disease_button_kb_uz())
        bot.register_next_step_handler(message, get_vac_disease_uz, sex, age)
def get_vac_disease_uz(message, sex, age):
    user_id = message.from_user.id
    disease = message.text
    if disease == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Қуйида келтирилган ишлардан нечтасини одам мустақил бажара олади?\n"
                                  "1.	Озиқ-овқатни енгил тайёрлаш\n"
                                  "2.	Кийиниш ва ечиниш\n"
                                  "3.	Чўмилиш\n"
                                  "4.	Ҳожатга қатнаш ва ўз-ўзини тартибга солиш",
                         reply_markup=hamrohbuttons.severity_button_kb_uz())
        bot.register_next_step_handler(message, get_vac_severity_uz, sex, age, disease)
def get_vac_severity_uz(message, sex, age, disease):
    user_id = message.from_user.id
    severity = message.text
    if severity == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Уй кўмакчиси кунига неча соат давомида сизга керак бўлади?",
                         reply_markup=hamrohbuttons.schedule_button_kb_uz())
        bot.register_next_step_handler(message, get_vac_schedule_uz, sex, age, disease, severity)
def get_vac_schedule_uz(message, sex, age, disease, severity):
    user_id = message.from_user.id
    schedule = message.text
    if schedule == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Кўмакчининг қўчимча хўжалик ишларида (тозалаш, кир ювиш, овқат тайёрлаш, дўконга харид учун чиқиш ва ҳ.к.) ёрдамига муҳтожмисиз",
                         reply_markup=hamrohbuttons.extrawork_button_kb_uz())
        bot.register_next_step_handler(message, get_vac_extrawork_uz, sex, age, disease, severity, schedule)
def get_vac_extrawork_uz(message, sex, age, disease, severity, schedule):
    user_id = message.from_user.id
    extra_work = message.text
    if extra_work == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Кўмакчи сизга қайси муддат давомида керак?",
                         reply_markup=hamrohbuttons.period_button_kb_uz())
        bot.register_next_step_handler(message, get_vac_period_uz, sex, age, disease, severity, schedule, extra_work)
def get_vac_period_uz(message, sex, age, disease, severity, schedule, extra_work):
    user_id = message.from_user.id
    period = message.text
    if period == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Менюдаги тугма ёрдамида ўз рақамингизни жунатинг",
                         reply_markup=hamrohbuttons.num_button_kb_uz())
        bot.register_next_step_handler(message, get_vac_phone_number_uz, sex, age, disease, severity, schedule, extra_work,
                                   period)

def get_vac_phone_number_uz(message, sex, age, disease, severity, schedule, extra_work, period):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, "Қуйида манзил, хусусан туман номи ва яқин мўлжални ёзинг." 
                                  "(геолокация жўнатманг). Ҳамда Сиз муҳим деб топган ҳар қандай маълумотни қолдиришингиз мумкин", reply_markup=hamrohbuttons.main_menu_reply_kb_uz())
        bot.register_next_step_handler(message, get_vac_address_uz, sex, age, disease, severity, schedule, extra_work,
                                       period, phone_number)
    elif message.text == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Тугма орқали ўз рақамингизни жўнатманг")
        bot.register_next_step_handler(message, get_vac_phone_number_uz, sex, age, disease, severity, schedule, extra_work,
                                       period)

def get_vac_address_uz(message,sex, age, disease, severity, schedule, extra_work, period, phone_number):
    user_id = message.from_user.id
    address = message.text
    if address == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Юқорида келтирилган жавоблардан келиб чиқиб, кўмакчи хизмати учун тўлашга тайёр бўлган нархни ёзинг", reply_markup=hamrohbuttons.main_menu_reply_kb())
        bot.register_next_step_handler(message, get_vac_salary_uz, sex, age, disease, severity, schedule, extra_work,
                                   period, phone_number, address)
def get_vac_salary_uz(message, sex, age, disease, severity, schedule, extra_work, period, phone_number, address):
    user_id = message.from_user.id
    salary = message.text
    if salary == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Сўровингиз жўнатилди", reply_markup=types.ReplyKeyboardRemove())
        posting = bot.send_message(-1001925064725, f"<b>Жинс</b>: {sex}\n"
                                                   f"<b>Ёш</b>: {age}\n"
                                                   f"<b>Касаллик</b>: {disease}\n"
                                                   f"<b>Мустақиллик даражаси(4 балли шкала)</b>: {severity}\n"
                                                   f"<b>Иш куни</b>: {schedule}\n"
                                                   f"<b>Қўшимча иш</b>: {extra_work}\n"
                                                   f"<b>Иш даври</b>: {period}\n"
                                                   f"<b>Манзил ва қўшимча маълумот</b>: {address}\n"
                                                   f"<b>Тўлов</b>: {salary}\n"
                                                   f"<b>Телефон</b>: {phone_number}", parse_mode="html")
        message_id = posting.message_id
        hamrohdatabase.add_vac(user_id, sex, age, disease, severity, schedule, extra_work, period,
                               phone_number, address, salary, message_id)
        start_message(message)
def take_question_uz(message):
    user_id = message.from_user.id
    question = message.text
    if question == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Сўровингиз жўнатилди. Сизга яқин вақт оралиғида жавоб беришади",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(305896408, f"{user_id} дан савол\n\n"
                                f"Савол: {question}")
        start_message(message)
def get_nurse_name_uz(message):
    user_id = message.from_user.id
    name = message.text
    if name == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Ўз жинсингизни танланг", reply_markup=hamrohbuttons.gender_kb_uz())
        bot.register_next_step_handler(message, get_nurse_gender_uz, name)
def get_nurse_gender_uz(message, name):
    user_id = message.from_user.id
    sex = message.text
    if sex == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Туғилган йилингизни ёзинг", reply_markup=hamrohbuttons.main_menu_reply_kb_uz())
        bot.register_next_step_handler(message, get_nurse_age_uz, name, sex)
def get_nurse_age_uz(message, name, sex):
    user_id = message.from_user.id
    age = message.text
    if age == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Ўз маълумотингиз ва мутахассислигингиз ҳақида қисқа ва аниқ ёзинг",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_nurse_education_uz, name, sex, age)
def get_nurse_education_uz(message, name, sex, age):
    user_id = message.from_user.id
    education = message.text
    if education == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Бемор одамлар парвариши билан боғлиқ иш тажрибангиз ҳақида қисқа ва аниқ маълумот ёзинг. "
                                 "Неча йил ва қандай одамлар билан ишлаганингиз ҳақида ёзинг. Бир неча жойда ишлаган бўлсангиз, ҳар бир тажрибангизни тартиб рақамлар (1. 2. 3.) билан ажратсангиз бўлади.",
                         reply_markup=hamrohbuttons.main_menu_reply_kb_uz())
        bot.register_next_step_handler(message, get_nurse_experience_uz, name, sex, age, education)
def get_nurse_experience_uz(message, name, sex, age, education):
    user_id = message.from_user.id
    experience = message.text
    if experience == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Уйдаги парваришда ёрдам бериши мумкин бўлган кўникмаларингиз ҳақида ёзинг.Ҳамда Сиз муҳим деб топган ҳар қандай маълумотни қолдиришингиз мумкин",
                         reply_markup=hamrohbuttons.main_menu_reply_kb_uz())
        bot.register_next_step_handler(message, get_nurse_skills_uz, name, sex, age, education, experience)
def get_nurse_skills_uz(message, name, sex, age, education, experience):
    user_id = message.from_user.id
    skills = message.text
    if skills == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Турар манзилингиз, хусусан туманни ёзинг (геолокацияни жўнатманг)",
                         reply_markup=hamrohbuttons.main_menu_reply_kb_uz())
        bot.register_next_step_handler(message, get_nurse_address_uz, name, sex, age, education, experience, skills)
def get_nurse_address_uz(message, name, sex, age, education, experience, skills):
    user_id = message.from_user.id
    address = message.text
    if address == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Менюдаги тугма ёрдамида ўз рақамингизни жўнатинг",
                         reply_markup=hamrohbuttons.num_button_kb_uz())
        bot.register_next_step_handler(message, get_nurse_phone_number_uz, name, sex, age, education, experience, skills, address)
def get_nurse_phone_number_uz(message, name, sex, age, education, experience, skills, address):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, "Ўз фотосуратингизни юкланг. "
                                  "Яхши ёритилган, сифатли фотосурат бўлиши керак. "
                                  "Жилмайишни унутманг ",
                         reply_markup=hamrohbuttons.main_menu_reply_kb_uz())
        bot.register_next_step_handler(message, get_nurse_photo_uz, name, sex, age, education, experience, skills,
                                       address, phone_number)
    elif message.text == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Тугма ёрдамида ўз рақамингизни жўнатинг")
        bot.register_next_step_handler(message, get_nurse_phone_number_uz, name, sex, age, education,
                                       experience, skills, address)
def get_nurse_photo_uz(message,name, sex, age, education, experience, skills, address, phone_number):
    user_id = message.from_user.id
    if message.photo:
        photo = message.photo[-1].file_id
        bot.send_message(user_id, "Анкетангиз тайёр",
                         reply_markup=types.ReplyKeyboardRemove())
        posting = bot.send_photo(-1001905443362, photo=photo, caption=f"{name}\n"
                                                                      f"<b>Жинс</b>: {sex}\n"
                                                                      f"<b>Ёш</b>: {age}\n"
                                                                      f"<b>Маълумот</b>: {education}\n"
                                                                      f"<b>Иш тажрибаси</b>: {experience}\n"
                                                                      f"<b>Кўникмалар ва қўшимча маълумот</b>: {skills}\n"
                                                                      f"<b>Манзил</b>: {address}\n"
                                                                      f"<b>Телефон рақами</b>: {phone_number}",
                                 parse_mode="html")
        message_id = posting.message_id

        hamrohdatabase.add_nurse(user_id, name, sex, age, education, experience, skills, address, phone_number, photo,
                                 message_id)
        # photo = hamrohdatabase.get_nurses_photo(user_id)
        # bot.send_photo(user_id, photo=photo[0])
        start_message(message)
    elif message.text == "Бош меню":
        start_message(message)
    else:
        bot.send_message(user_id, "Фотосуратни жўнатинг")
        bot.register_next_step_handler(message, get_nurse_phone_number_uz, name, sex, age, education,
                                       experience, skills, address)


@bot.message_handler(commands=["admin"])
def admin_panel(message):
    user_id = message.from_user.id
    checker = hamrohdatabase.check_admin(user_id)
    types.ReplyKeyboardRemove()
    if checker == True:
        bot.send_message(user_id, "Админ панель. Выберите действие",
                         reply_markup=hamrohbuttons.main_admin_menu())
    else:
        pass


# open(file, 'rb')
bot.polling(non_stop=True)
