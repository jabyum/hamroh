import sqlite3
from datetime import datetime
connection = sqlite3.connect("hamrohbotbase.db")
sql = connection.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS all_users (tg_id INTEGER, language TEXT, user_reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS vacancies (vac_id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER, "
            "sex TEXT, age TEXT, disease TEXT, severity INTEGER, schedule TEXT, extra_work TEXT, "
            "period TEXT, phone_number TEXT, address TEXT, salary TEXT, message_id INTEGER, vac_reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS nurses (nurse_id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER, name TEXT, "
            "sex TEXT, age TEXT, education TEXT, experience TEXT, skills TEXT, address TEXT,"
            "phone_number TEXT, photo BLOB NOT NULL, message_id INTEGER, nurse_reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS admins (admin_id INTEGER, rank INTEGER, admin_reg_date DATETIME);")

connection.commit()
def reg_user(user_id, language):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO all_users (tg_id, language, user_reg_date) "
                "VALUES (?, ?, ?);", (user_id, language, datetime.now()))
    connection.commit()

def check_language(user_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT language FROM all_users WHERE tg_id=?;", (user_id,))
    if checker.fetchone() == ("uzb",):
        return "uzb"
    elif checker.fetchone() == ("rus",):
        return "rus"
    return False
def change_language(language, user_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    sql.execute("UPDATE all_users SET language=? WHERE tg_id=?;", (language, user_id))
    connection.commit()
def check_vac(user_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT tg_id FROM vacancies WHERE tg_id=?;", (user_id, ))
    if checker.fetchone():
        return True
    else:
        return False
def check_nurse(user_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT tg_id FROM nurses WHERE tg_id=?;", (user_id, ))
    if checker.fetchone():
        return True
    else:
        return False
def add_nurse(user_id, name, sex, age, education, experience, skills, address, phone_number, photo, message_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO nurses (tg_id, name, sex, age, education, experience, skills, address, "
                "phone_number, photo, message_id, nurse_reg_date) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, name, sex, age, education, experience,
                                                              skills, address, phone_number, photo, message_id,
                                                                 datetime.now()))
    connection.commit()
def add_vac(user_id, sex, age, disease, severity, schedule, extra_work, period, phone_number, address, salary, message_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO vacancies (tg_id, sex, age, disease, severity, schedule, extra_work, period, "
                "phone_number, address, salary, message_id, vac_reg_date) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, sex, age, disease, severity, schedule,
                                                                 extra_work, period, phone_number, address, salary,
                                                                 message_id, datetime.now()))
    connection.commit()
def get_nurses_photo(tg_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    photo = sql.execute("SELECT photo FROM nurses WHERE tg_id=?;", (tg_id, )).fetchone()
    return photo
def get_nurse_db(tg_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    exact_user = sql.execute("SELECT tg_id, name, sex, age, education, experience, skills, address, "
                "phone_number, photo, nurse_reg_date FROM nurses WHERE tg_id=?;", (tg_id,)).fetchone()
    return exact_user
def get_nurse_message_id(user_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    nurse_message_id = sql.execute("SELECT message_id FROM nurses WHERE tg_id=?;", (user_id,)).fetchone()
    return nurse_message_id
def get_vacancy_message_id(user_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    vacancy_message_id = sql.execute("SELECT message_id FROM vacancies WHERE tg_id=?;", (user_id,)).fetchone()
    return vacancy_message_id
def delete_exact_nurse(user_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM nurses WHERE tg_id=?;", (user_id, ))
    connection.commit()
def delete_exact_vacancie(user_id):
    connection = sqlite3.connect("hamrohbotbase.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM vacancies WHERE tg_id=?;", (user_id, ))
    connection.commit()
