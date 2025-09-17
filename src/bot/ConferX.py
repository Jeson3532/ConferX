# -- coding: utf-8
import time
import telebot
import webbrowser
from telebot import types
import traceback as tb
import requests
from pprint import pp
from datetime import datetime, timedelta
from telebot.handler_backends import State, StatesGroup
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv("TOKEN")
finalMsgs = dict()

def save_last_messages(chat, user, botmsg):
    finalMsgs[chat] = (user, botmsg)


bot = telebot.TeleBot(token)

auth_users = dict()
auth_users_list = list()

last_user = None


# Главное меню


def authorization(user):
    try:

        data = {
            "login": f"{auth_users[user]['login']}",
            "password": f"{auth_users[user]['password']}",
            "fingerprint": {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
                "webdriver": "",
                "language": "ru",
                "colorDepth": 24,
                "deviceMemory": 8,
                "hardwareConcurrency": 12,
                "screenHeight": 1920,
                "screenWidth": 1080,
                "timezoneOffset": -180,
                "timezone": "Europe/Moscow",
                "localStorage": True,
                "indexedDb": True,
                "openDatabase": True,
                "adBlock": True,
                "audio": "124.04347527516074",
                "hasLiedOs": None,
                "hasLiedBrowser": None,
                "hasLiedLanguages": None,
                "hasLiedResolution": None,
                "hasTouchSupport": None
            }
        }

        response = requests.post("https://test.vcc.uriit.ru/api/auth/login", json=data)

        token = response.json().get("token")

        return token
    except:
        tb.print_exc()
        return None


def auth_setParams(user):
    try:
        auth_users[user]["lastmsgtime"] = time.time()

        auth_users[user]["lastbotmsg"] = None
        auth_users[user]["msgfordelete"] = list()
        auth_users[user]["FirstDate"] = "Не указано"
        auth_users[user]["LastDate"] = "Не указано"
        auth_users[user]["FirstDateBool"] = True
        auth_users[user]["FilterFastDate"] = False
        auth_users[user]["Filter"] = "Не выбрано"
        auth_users[user]["Status"] = "Не выбрано"
        auth_users[user]["StepOpros"] = 1
        auth_users[user]["IDsBuild"] = list()
        auth_users[user]["IDsRoom"] = list()
        auth_users[user]["BuildBool"] = False
        auth_users[user]["ToContinue"] = False
        auth_users[user]["ContinueBool"] = False
        auth_users[user]["FirstParams"] = dict()
        auth_users[user]["FirstParams"] = {
            "fromDatetime": None,
            "toDatetime": None,
            "state": None,
            "filter": None,
            "departmentId": None,
            "userId": None,
            "userParticipant": None,
            "priority": None
        }
        auth_users[user]["DepartParams"] = dict()
        auth_users[user]["DepartParams"] = {
            "name": None
        }

        auth_users[user]["CreateParams"] = {
            "name": None,
            "buildId": None,  # Айди здания, а не комнаты!!!
            "roomId": None,
            "startedAt": None,
            "duration": None,
            "participants": list(dict()),
            "participantsEmails": list(),
            "participantsCount": None,
            "backend": None


    }
    except:
        print("Error")


def menuDates(user, messageId, message):
    try:
        auth_users[user]["FirstDateBool"] = True
        auth_users[user]["FirstDate"] = "Не указано"
        auth_users[user]["LastDate"] = "Не указано"

        bot.send_message(messageId,
                         f"<b>━━━━━━━━━━🌟━━━━━━━━━━</b>\n\n📅 Укажите <b>начало периода проведения</b> ВКС, либо же <b>воспользуйтесь кнопками быстрой фильтрации</b>. \n\n🔎 Начало: <b>{auth_users[user]['FirstDate']}</b>\n🔍 Конец: <b>{auth_users[user]['LastDate']}</b>\n🕒 Пример: <i>07.11.2024</i>\n<b>━━━━━━━━━━✨━━━━━━━━━━</b>",
                         reply_markup=addFastFilterButtons(), parse_mode="html")

        bot.register_next_step_handler(message, dateHandler)
    except:
        print("Error dates")


def addMainButtons(user):
    try:
        m = types.ReplyKeyboardMarkup()
        auth_users[user]["Filter"] = "Не выбрано"
        auth_users[user]["Status"] = "Не выбрано"
        bt1 = types.InlineKeyboardButton("Просмотр ВКС")
        bt2 = types.InlineKeyboardButton("Указать дату")
        m.row(bt1, bt2)
        bt3 = types.InlineKeyboardButton("Посмотреть мои ВКС")
        bt4 = types.InlineKeyboardButton("Посмотреть ВКС моей организации")
        m.row(bt3, bt4)
        bt6 = types.InlineKeyboardButton("Создать ВКС")
        bt5 = types.InlineKeyboardButton("Справка")
        m.row(bt6)
        m.row(bt5)
        return m
    except:
        print("Error")


def addFilterButtonsMAIN():
    try:
        m = types.ReplyKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Состояние", callback_data="status")
        button2 = types.InlineKeyboardButton("Наименование", callback_data="name")
        m.row(button1, button2)
        button3 = types.InlineKeyboardButton("Приоритет", callback_data="priority")
        button4 = types.InlineKeyboardButton("Департамент", callback_data="dep")
        button5 = types.InlineKeyboardButton("Организатор", callback_data="head")
        m.row(button3, button4)

        m.row(button5)

        return m
    except:
        print("Error")


def addPriorityButtons():
    try:
        m = types.ReplyKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Низкий", callback_data="status")
        button2 = types.InlineKeyboardButton("Средний", callback_data="name")
        m.row(button1, button2)
        button3 = types.InlineKeyboardButton("Высокий", callback_data="priority")
        m.row(button3)

        return m
    except:
        print("Error")


def addFilterButtons():
    try:
        Button1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Button1.add("Забронированные")
        Button1.add("Начатые")
        Button1.add("Законченные")
        Button1.add("Отмененные")
        return Button1
    except:
        print("Error")


def addBackendButtons():
    try:
        Button1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Button1.add("Cisco")
        Button1.add("Permanentroom")
        Button1.row()
        Button1.add("External")
        Button1.add("Vinteo")
        return Button1
    except:
        print("Error")


def addContinueButtons():
    try:
        Button1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Button1.add("Продолжить")
        Button1.row()
        Button1.add("Меню выбора дат")

        return Button1
    except:
        print("Error")


def addFastFilterButtons():
    try:
        keyboard = types.InlineKeyboardMarkup()

        bt1 = types.InlineKeyboardButton(text="За сегодня", callback_data="FastToday")
        bt2 = types.InlineKeyboardButton(text="За неделю", callback_data="FastWeek")
        bt3 = types.InlineKeyboardButton(text="За месяц", callback_data="FastMonth")
        bt4 = types.InlineKeyboardButton(text="Отмена", callback_data="CancelDate")

        keyboard.row(bt1, bt2, bt3)
        keyboard.row(bt4)

        return keyboard
    except:
        print("Error")


def addReadyButtons():
    try:
        m = types.ReplyKeyboardMarkup()
        button1 = m.add("Готово")
        button2 = m.add("Отмена")
        m.row(button1, button2)

        return m
    except:
        print("Error")


def addButtonsDaNet():
    try:
        Button1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Button1.add("Да")
        Button1.add("Нет")
        Button1.row()

        keyboard = types.InlineKeyboardMarkup()

        bt1 = types.InlineKeyboardButton(text="Кнопка 1", callback_data="OnBuild")

        keyboard.add(bt1)
        return Button1
    except:
        print("Error")


def addSettingsButton(user):
    try:
        keyboard = types.InlineKeyboardMarkup()
        if auth_users[user]["BuildBoolButton"]:
            bt1 = types.InlineKeyboardButton(text="Место проведения: ВКЛ", callback_data="OnBuild")
            auth_users[user]["BuildBoolButton"] = False
            auth_users[user]["BuildBool"] = True
        else:
            bt1 = types.InlineKeyboardButton(text="Место проведения: ВЫКЛ", callback_data="OnBuild")
            auth_users[user]["BuildBoolButton"] = True
            auth_users[user]["BuildBool"] = False

        keyboard.add(bt1)
        return keyboard
    except:
        print("Error")


def addCreateButtons():
    try:
        keyboard = types.InlineKeyboardMarkup()

        bt1 = types.InlineKeyboardButton(text="Создать конференцию", callback_data="CreateConf")
        bt2 = types.InlineKeyboardButton(text="Отмена", callback_data="Cancel")

        keyboard.add(bt1, bt2)
        return keyboard
    except:
        print("Error")


def addSearchButtons():
    try:
        keyboard = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton(text="Изменить фильтрацию", callback_data="ChangeFilter")
        bt2 = types.InlineKeyboardButton(text="Начать поиск", callback_data="Search")

        keyboard.add(bt1, bt2)
        return keyboard
    except:
        print("Error")


def sbros_Date(user):
    try:
        auth_users[user]["FirstDate"] = "Не указано"
        auth_users[user]["LastDate"] = "Не указано"
        auth_users[user]["FirstParams"] = {
            "fromDatetime": None,
            "toDatetime": None,
        }
    except:
        print("Error")


def sbros(user):
    try:
        auth = last_user in auth_users_list
        if auth:
            auth_users[user]['BuildBool'] = False
            auth_users[user]['ToContinue'] = False
            auth_users[user]["IDsRoom"] = list()
            auth_users[user]["IDsBuild"] = list()
        #     auth_users[user]["FirstParams"] = {
        #         "fromDatetime": f"{auth_users[user]['FirstDate']}T00:00:00.00",
        #         "toDatetime": f"{auth_users[user]['LastDate']}T23:59:59.00",
        #         "state": None,
        #         "filter": None,
        #         "priority": None
        # }
        bot.clear_step_handler_by_chat_id(user)
    except:
        print("Error")


def openButtonVKS(message):
    try:
        user = message.chat.id

        if auth_users[user]["Filter"] == "Состояние":
            bot.send_message(message.chat.id,
                             f"<b>┏━━━━━━━━━━━━┓ ┏━━━━━━━━━━━━━━┓\n┃Фильтрация запросов        ┃Выберите желаемый фильтр</b>\n┗━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━┛\n"
                             f"<b>➤| Текущая фильтрация</b>: {auth_users[user]['Filter']}\n"
                             f"<b>➤| Состояние</b>: {auth_users[user]['Status']}\n"
                             f"<b>📅| Период</b>: \n"
                             f"- Начало: <i>{auth_users[user]['FirstDate']}</i>\n"
                             f"- Конец: <i>{auth_users[user]['LastDate']}</i>\n"
                             f"📌 Для начала поиска <b>воспользуйтесь кнопкой ниже.</b>",
                             reply_markup=addSearchButtons(), parse_mode="html")
        elif auth_users[user]["Filter"] == "Наименование":
            bot.send_message(message.chat.id,
                             f"<b>┏━━━━━━━━━━━━┓ ┏━━━━━━━━━━━━━━┓\n┃Фильтрация запросов        ┃Выберите желаемый фильтр</b>\n┗━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━┛\n"
                             f"<b>➤| Текущая фильтрация</b>: {auth_users[user]['Filter']}\n"
                             f"<b>➤| Название</b>: {auth_users[user]['FirstParams']['filter']}\n"
                             f"<b>📅| Период</b>: \n"
                             f"- Начало: <i>{auth_users[user]['FirstDate']}</i>\n"
                             f"- Конец: <i>{auth_users[user]['LastDate']}</i>\n"
                             f"📌 Для начала поиска <b>воспользуйтесь кнопкой ниже.</b>",
                             reply_markup=addSearchButtons(), parse_mode="html")
        elif auth_users[user]["Filter"] == "Приоритет":
            bot.send_message(message.chat.id,
                             f"<b>┏━━━━━━━━━━━━┓ ┏━━━━━━━━━━━━━━┓\n┃Фильтрация запросов        ┃Выберите желаемый фильтр</b>\n┗━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━┛\n"
                             f"<b>➤| Текущая фильтрация</b>: {auth_users[user]['Filter']}\n"
                             f"<b>➤| Приоритет</b>: {auth_users[user]['FirstParams']['priority']}\n"
                             f"<b>📅| Период</b>: \n"
                             f"- Начало: <i>{auth_users[user]['FirstDate']}</i>\n"
                             f"- Конец: <i>{auth_users[user]['LastDate']}</i>\n"
                             f"📌 Для начала поиска <b>воспользуйтесь кнопкой ниже.</b>",
                             reply_markup=addSearchButtons(), parse_mode="html")
        else:
            bot.send_message(message.chat.id,
                             f"<b>┏━━━━━━━━━━━━┓ ┏━━━━━━━━━━━━━━┓\n┃Фильтрация запросов        ┃Выберите желаемый фильтр</b>\n┗━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━┛\n"
                             f"<b>➤| Текущая фильтрация</b>: {auth_users[user]['Filter']}\n"
                             f"<b>📅| Период</b>: \n"
                             f"- Начало: <i>{auth_users[user]['FirstDate']}</i>\n"
                             f"- Конец: <i>{auth_users[user]['LastDate']}</i>\n"
                             f"📌 Для начала поиска <b>воспользуйтесь кнопкой ниже.</b>",
                             reply_markup=addSearchButtons(), parse_mode="html")
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        print("Error")



@bot.message_handler(commands=['exit'])
def exit_account(message):
    try:
        auth = last_user in auth_users_list
        user = message.chat.id
        if auth:
            bot.send_message(message.chat.id, "<b>➤|Вы вышли из учетной записи</b>.", parse_mode="html")
            auth_users_list.remove(user)
        else:
            bot.send_message(message.chat.id, "<b>🔸| Ошибка! Вы не авторизованы</b>.", parse_mode="html")
    except:
        tb.print_exc()
        print("Error")


@bot.message_handler(commands=['start'])
def send(message):
    try:
        user = message.chat.id
        auth = last_user in auth_users_list
        if auth:
            sbros(user)
            bot.send_message(message.chat.id,
                             "👋 Приветствую, " + f"<b>{message.from_user.first_name}</b>! Выбери <b>то</b>, что тебя <b>интересует</b>:",
                             parse_mode="html", reply_markup=addMainButtons(user))
            bot.register_next_step_handler(message, clickButton)
        else:
            bot.send_message(message.chat.id,
                             f"👋 Приветствую, <b>{message.from_user.first_name}</b>! Чтобы <b>пользоваться функционалом</b> этого бота требуется <b>авторизация</b>.\n🔔Авторизоваться можно, используя команду <b>/login</b> <i>имя_пользователя пароль_пользователя</i>.",
                             parse_mode="html")
    except:
        print("Error")


@bot.message_handler(commands=['cancel', 'stop', 'c'])
def send(message):
    try:
        user = message.chat.id
        auth = last_user in auth_users_list
        if auth:
            sbros(user)
            bot.send_message(message.chat.id, "<b>💫| Отменил все текущие действия</b>. Выберите то, что Вас интересует:",
                             parse_mode="html", reply_markup=addMainButtons(user))
            bot.register_next_step_handler(message, clickButton)
        else:
            bot.send_message(message.chat.id,
                             f"👋 Приветствую, <b>{message.from_user.first_name}</b>! Чтобы <b>пользоваться функционалом</b> этого бота требуется <b>авторизация</b>.\n🔔Авторизоваться можно, используя команду <b>/login</b> <i>имя_пользователя пароль_пользователя</i>.",
                             parse_mode="html")
    except:
        print("Error")



# Клик по кнопкам
def clickButton(message):
    try:
        user = message.chat.id

        currentTime = time.time()
        if currentTime - auth_users[user]["lastmsgtime"] > 1:

            auth_users[user]["lastmsgtime"] = time.time()

            if message.text == "Указать дату":
                menuDates(user, message.chat.id, message)
            elif message.text == "Просмотр ВКС":
                if auth_users[user]["FirstParams"]["fromDatetime"] and auth_users[user]["FirstParams"][
                    "fromDatetime"] != "Не указаноT00:00:00.00":
                    openButtonVKS(message)
                else:
                    bot.send_message(message.chat.id,
                                     " <b>🔸| Вы не выбрали период для фильтрации!</b> Хотите <b>продолжить</b> или перейти к <b>меню выбора дат</b>?",
                                     parse_mode="html", reply_markup=addContinueButtons())
                    auth_users[user]["ToContinue"] = True
            elif message.text == "Посмотреть мои ВКС":
                # Загрузка данных из requests.get()

                headers = {
                    "Authorization": f"Bearer {authorization(user)}"
                }
                # Получение своего айди
                response_acc = requests.get("https://test.vcc.uriit.ru/api/account/user-info", headers=headers)

                auth_users[user]["FirstParams"]["userParticipant"] = response_acc.json()["id"]
                auth_users[user]["FirstParams"]["fromDatetime"] = f"1000-01-01T00:00:00.00"
                auth_users[user]["FirstParams"]["toDatetime"] = f"5000-01-01T00:00:00.00"

                bot.send_message(message.chat.id, "⏳| <b>Загружаю список Ваших ВКС за всё время...</b>", parse_mode="html")
                response_rooms = requests.get("https://test.vcc.uriit.ru/api/meetings", headers=headers,
                                              params=auth_users[user]["FirstParams"])
                pp(response_rooms.text)
                if response_rooms:
                    finalMsgLast = ""
                    number = 1
                    for lst in response_rooms.json()["data"]:

                        # Имя ВКС
                        name = lst["name"]
                        # Айди комнаты
                        roomId = lst["id"]
                        # Дата и время начала
                        createdAt = lst["createdAt"]
                        # Продолжительность
                        dur = lst["duration"]
                        if dur >= 60:
                            dur = str(lst["duration"] // 60) + " ч."
                        else:
                            dur = str(lst["duration"]) + " мин."

                        params = {
                            "organizedUser": {
                                "firstname": "Никита",
                                "lastName": "Платинов"
                            }
                        }

                        response_idroom = requests.get(f"https://test.vcc.uriit.ru/api/meetings/{roomId}",
                                                       headers=headers)

                        # Место проведения
                        field = response_idroom.json()["room"]
                        if field:
                            field = response_idroom.json()["room"]["name"]
                        else:
                            field = "Отсутствует"
                        # Имя организатора
                        orgUser = f'{response_idroom.json()["organizedUser"]["firstName"]} {response_idroom.json()["organizedUser"]["lastName"]}'
                        # Список участников
                        participants = list()
                        for ls in response_idroom.json()["participants"]:
                            firstName, lastName = ls["firstName"], ls["lastName"]
                            participants.append(f"{firstName} {lastName}")
                        # Средство проведения
                        platform = response_idroom.json()["backend"]

                        finalMsg = {
                            "🗒<b>Название ВКС</b>:": f'"{name}"',
                            "🏢<b>Место проведения</b>:": f"{field}",
                            "🗓<b>Дата и время начала</b>:": f"{createdAt.split('T')[0]} {createdAt.split('T')[1].split(':')[0]}:{createdAt.split('T')[1].split(':')[1]}",
                            "🕑<b>Продолжительность</b>:": f"{dur}",
                            "👤<b>Организатор</b>:": f"{orgUser}",
                            "👥<b>Участники</b>:": "\n- <i>" + '\n- '.join(participants) + "</i>",
                            "ℹ️<b>Средство проведения</b>:": f"{platform}",
                        }

                        text = ""
                        for index, word in finalMsg.items():
                            text = text + f"{index} {word}" + "\n"
                        part = text
                        if len(finalMsgLast) + len(part) > 4096:
                            bot.send_message(message.chat.id,
                                             f"<b>┏━━━━━━━━━━━━┓\n┃ Список Ваших ВКС №{number}📩</b>\n┗━━━━━━━━━━━━┛\n{finalMsgLast}",
                                             parse_mode="html")
                            finalMsgLast = ""
                            number += 1
                        else:
                            finalMsgLast = finalMsgLast + "\n" + "".join(text)
                    if finalMsgLast:
                        bot.send_message(message.chat.id,
                                         f"<b>┏━━━━━━━━━━━━┓\n┃ Список Ваших ВКС №{number}📩</b>\n┗━━━━━━━━━━━━┛\n{finalMsgLast}",
                                         parse_mode="html")
                    else:
                        bot.send_message(message.chat.id, "🔸| По заданным параметрам <b>ничего на найдено</b>.",
                                         parse_mode="html")

                    auth_users[user]["FirstParams"]["userParticipant"] = None
                    auth_users[user]["FirstParams"]["fromDatetime"] = f"{auth_users[user]['FirstDate']}T00:00:00.00"
                    auth_users[user]["FirstParams"]["toDatetime"] = f"{auth_users[user]['LastDate']}T23:59:59.00"
                    bot.register_next_step_handler(message, clickButton)

            elif message.text == "Посмотреть ВКС моей организации":

                headers = {
                    "Authorization": f"Bearer {authorization(user)}"
                }
                # Получение своего айди
                response_acc = requests.get("https://test.vcc.uriit.ru/api/account/user-info", headers=headers)

                auth_users[user]["FirstParams"]["departmentId"] = response_acc.json()["departmentId"]
                auth_users[user]["FirstParams"]["fromDatetime"] = f"1000-01-01T00:00:00.00"
                auth_users[user]["FirstParams"]["toDatetime"] = f"5000-01-01T00:00:00.00"

                bot.send_message(message.chat.id, "⏳| <b>Загружаю список ВКС Вашей организации за всё время...</b>",
                                 parse_mode="html")
                response_rooms = requests.get("https://test.vcc.uriit.ru/api/meetings", headers=headers,
                                              params=auth_users[user]["FirstParams"])
                pp(response_rooms.text)
                if response_rooms:
                    finalMsgLast = ""
                    number = 1
                    for lst in response_rooms.json()["data"]:

                        # Имя ВКС
                        name = lst["name"]
                        # Айди комнаты
                        roomId = lst["id"]
                        # Дата и время начала
                        createdAt = lst["createdAt"]
                        # Продолжительность
                        dur = lst["duration"]
                        if dur >= 60:
                            dur = str(lst["duration"] // 60) + " ч."
                        else:
                            dur = str(lst["duration"]) + " мин."

                        params = {
                            "organizedUser": {
                                "firstname": "Никита",
                                "lastName": "Платинов"
                            }
                        }

                        response_idroom = requests.get(f"https://test.vcc.uriit.ru/api/meetings/{roomId}",
                                                       headers=headers)
                        response_getName = requests.get(
                            f"https://test.vcc.uriit.ru/api/catalogs/departments/{response_acc.json()['departmentId']}",
                            headers=headers)

                        # Место проведения
                        field = response_idroom.json()["room"]
                        if field:
                            field = response_idroom.json()["room"]["name"]
                        else:
                            field = "Отсутствует"
                        # Имя организатора
                        orgUser = f'{response_idroom.json()["organizedUser"]["firstName"]} {response_idroom.json()["organizedUser"]["lastName"]}'
                        # Список участников
                        participants = list()
                        for ls in response_idroom.json()["participants"]:
                            firstName, lastName = ls["firstName"], ls["lastName"]
                            participants.append(f"{firstName} {lastName}")
                        # Средство проведения
                        platform = response_idroom.json()["backend"]

                        finalMsg = {
                            "🗒<b>Название ВКС</b>:": f'"{name}"',
                            "🏢<b>Место проведения</b>:": f"{field}",
                            "🗓<b>Дата и время начала</b>:": f"{createdAt.split('T')[0]} {createdAt.split('T')[1].split(':')[0]}:{createdAt.split('T')[1].split(':')[1]}",
                            "🕑<b>Продолжительность</b>:": f"{dur}",
                            "👤<b>Организатор</b>:": f"{orgUser}",
                            "👥<b>Участники</b>:": "\n- <i>" + '\n- '.join(participants) + "</i>",
                            "ℹ️<b>Средство проведения</b>:": f"{platform}",
                        }

                        text = ""
                        for index, word in finalMsg.items():
                            text = text + f"{index} {word}" + "\n"
                        part = text
                        if len(finalMsgLast) + len(part) > 4096:
                            bot.send_message(message.chat.id,
                                             f"<b>┏━━━━━━━━━━━━━━━━━━━━┓</b>\n<b>┃ Список ВКС Вашей организации №{number}📩</b>\n┗━━━━━━━━━━━━━━━━━━━━┛\n📍Ваша организация: <b>{response_getName.json()['shortName']}</b>\n{finalMsgLast}",
                                             parse_mode="html")
                            finalMsgLast = ""
                            number += 1
                        else:
                            finalMsgLast = finalMsgLast + "\n" + "".join(text)
                    if finalMsgLast:
                        bot.send_message(message.chat.id,
                                         f"<b>┏━━━━━━━━━━━━━━━━━━━━┓</b>\n<b>┃ Список ВКС Вашей организации №{number}📩</b>\n┗━━━━━━━━━━━━━━━━━━━━┛\n📍Ваша организация: <b>{response_getName.json()['shortName']}</b>\n{finalMsgLast}",
                                         parse_mode="html")

                    else:
                        bot.send_message(message.chat.id, "🔸| По заданным параметрам <b>ничего на найдено</b>.")

                    auth_users[user]["FirstParams"]["departmentId"] = None
                    auth_users[user]["FirstParams"]["fromDatetime"] = f"{auth_users[user]['FirstDate']}T00:00:00.00"
                    auth_users[user]["FirstParams"]["toDatetime"] = f"{auth_users[user]['LastDate']}T23:59:59.00"
                    bot.register_next_step_handler(message, clickButton)

            elif message.text == "Создать ВКС":
                auth_users[user]["BuildBoolButton"] = True
                auth_users[user]["BuildBool"] = True
                bot.send_message(message.chat.id, "👋Привет! Для <b>создания ВКС</b> понадобится следующая информация:\n"
                                                  "<b>- Название.</b>\n"
                                                  "<b>- Место проведения.</b>\n"
                                                  "<b>- Помещение.</b>\n"
                                                  "<b>- Дата и время начала.</b>\n"
                                                  "<b>- Продолжительность.</b>\n"
                                                  "<b>- Адреса участников.</b>\n"
                                                  "<b>- Максимальное количество участников.</b>\n"
                                                  "<b>- Средство проведения.</b>",

                                 parse_mode="html", reply_markup=addSettingsButton(user))
                bot.send_message(message.chat.id, "<b>➤| Готовы начать?</b>", parse_mode="html",
                                 reply_markup=addButtonsDaNet())
                bot.register_next_step_handler(message, DaNetHandler)
            # else:
            #     bot.send_message(message.chat.id, "➤| <b>Ничего не понял</b>! Выберите то, что Вас <b>интересует</b>:",
            #                      reply_markup=addMainButtons(user), parse_mode="html")
            #     bot.register_next_step_handler(message, clickButton)
        else:
            bot.send_message(message.chat.id, "<b>🔸| Подождите немного перед использованием!</b>", parse_mode="html",
                             reply_markup=addMainButtons(user))
            bot.register_next_step_handler(message, clickButton)
        # -*- coding: utf-8 -*-
        if message.text == "Справка":
            bot.send_message(message.chat.id,
                             """
                            <b>ConferX</b> - Бот для планирования видеоконференций.
            Этот бот предоставляет <b>удобный инструмент для создания, управления и просмотра видеоконференций</b> <i>(ВКС)</i> в вашей организации.
             С его помощью вы можете легко <b>планировать встречи, отслеживать информацию о проведенных и предстоящих ВКС, а также фильтровать события по различным критериям</b>.
        <b>Основные функции</b>:
             <b>📌Создание видеоконференций!</b>
            Создавайте новые видеоконференции, настраивая дату, время, участников, способ проведения и многого другого. Бот автоматически выдаст вам приглашение и разошлет напоминания на почту указанных участников.
    
             <b>📅Просмотр ВКС по фильтрам!</b>
            Используйте фильтры для поиска видеоконференций по дате, времени, участникам или статусу. Это позволяет быстро находить нужные встречи и управлять своим расписанием.
    
        <b>Доступные фильтры</b>:
            1. Состояние <i>(Забронированные, начатые, законченные, отмененные)</i>
            2. Наименование <i>(По названию или описанию)</i>
            3. По приоритету <i>(От низшего от высшего)</i>
            4. По департаменту <i>(Поиск по нужной организации)</i>
            5. Организатор <i>(Поиск по нужному организатору)</i>
    
             <b>💫Просмотр ВКС организации!</b>
            Получите список всех видеоконференций, запланированных в вашей организации. Это поможет отслеживать корпоративные события и синхронизировать мероприятия между коллегами.
    
             <b>🕒Просмотр своих ВКС!</b>
            Просматривайте все запланированные вами видеоконференции, чтобы отслеживать свои мероприятия и управлять ими в одном месте.
    
            ☑️| Этот бот <b>улучшает организацию встреч, сокращает время на планирование и помогает поддерживать эффективную коммуникацию в организации</b>""",
                             parse_mode="html")
            bot.register_next_step_handler(message, clickButton)
    except:
        print("Error")


def DaNetHandler(message):
    try:
        user = message.chat.id
        msg = message.text

        currentTime = time.time()
        if currentTime - auth_users[user]["lastmsgtime"] > 1:
            auth_users[user]["lastmsgtime"] = time.time()

            if msg.lower() == "да":

                auth_users[user]["CreateParams"] = {
                    "name": None,
                    "buildId": None,  # Айди здания, а не комнаты!!!
                    "roomId": None,
                    "startedAt": None,
                    "duration": None,
                    "participants": list(dict()),
                    "participantsEmails": list(),
                    "participantsCount": None,
                    "backend": None

                }

                bot_msg = bot.send_message(user, "➤| Введите <b>название</b> Вашей <b>ВКС</b>:", parse_mode="html",
                                           reply_markup=types.ReplyKeyboardRemove(True))
                auth_users[user]["lastbotmsg"] = bot_msg.message_id
                auth_users[user]["StepOpros"] = 1
                bot.register_next_step_handler(message, createVKSOpros)

            elif msg.lower() == "нет":
                bot.send_message(user, "<b>🔸| Возвращаю Вас в главное меню...</b>", parse_mode="html",
                                 reply_markup=addMainButtons(user))
                bot.register_next_step_handler(message, clickButton)
            else:
                bot.send_message(user, "<b>🔸| Ошибка! Дайте ответ на поставленный вопрос.</b>", parse_mode="html")
                bot.register_next_step_handler(message, DaNetHandler)
        else:
            bot.send_message(message.chat.id, "<b>🔸| Подождите немного перед использованием!</b>", parse_mode="html",
                             reply_markup=addButtonsDaNet())
    except:
        print("Error")


def createVKSOpros(message):
    try:
        user = message.chat.id
        auth_users[user]["msgfordelete"] = message.id

        currentTime = time.time()
        if currentTime - auth_users[user]["lastmsgtime"] > 1:
            auth_users[user]["lastmsgtime"] = time.time()
            if type(auth_users[user]["msgfordelete"]) == list:
                for i in auth_users[user]["msgfordelete"]:
                    bot.delete_message(user, i)
            if auth_users[user]["lastbotmsg"]:
                bot.delete_message(user, message.id)
                bot.delete_message(user, auth_users[user]["lastbotmsg"])
                auth_users[user]["lastbotmsg"] = None

            headers = {
                "Authorization": f"Bearer {authorization(user)}"
            }

            if auth_users[user]["BuildBool"]:
                if auth_users[user]["StepOpros"] == 1 and auth_users[user]["BuildBool"]:

                    if len(message.text) > 3:
                        auth_users[user]['CreateParams']['name'] = message.text

                        response_buildings = requests.get("https://test.vcc.uriit.ru/api/catalogs/buildings",
                                                          headers=headers)
                        finalMsgLast = ""
                        finalmsg = dict()
                        # Получение всех строений
                        for i in response_buildings.json()["data"]:
                            finalmsg[str("ID: " + str(i["id"]))] = f'➡ {i["name"]}'
                            auth_users[user]["IDsBuild"].append(str(i["id"]))

                        text = ""
                        for index, word in finalmsg.items():
                            text = text + f"{index} {word}" + "\n"
                        finalMsgLast = finalMsgLast + "\n" + "".join(text)

                        for i in range(0, len(finalMsgLast), 4096):
                            bot_msg = bot.send_message(message.chat.id,
                                                       "<b>☑️| Записано!</b>\nВыберите место проведения:\n" + finalMsgLast[
                                                                                                              i:i + 4096],
                                                       parse_mode="html")
                            auth_users[user]["lastbotmsg"] = bot_msg.message_id
                        auth_users[user]["StepOpros"] = 2
                    else:
                        bot.send_message(message.chat.id,
                                         "🔸| <b>Название ВКС</b> не может быть <b>меньше 3-х символов</b>!",
                                         parse_mode="html")

                elif auth_users[user]["StepOpros"] == 2:
                    if message.text in auth_users[user]["IDsBuild"]:
                        auth_users[user]["CreateParams"]["buildId"] = message.text

                        headers = {
                            "Authorization": f"Bearer {authorization(user)}"
                        }

                        response_rooms = requests.get("https://test.vcc.uriit.ru/api/catalogs/rooms", headers=headers)

                        finalMsgLast = ""
                        finalmsg = dict()

                        for i in response_rooms.json()["data"]:
                            if i["buildingId"] == int(auth_users[user]["CreateParams"]["buildId"]):
                                finalmsg["ID: " + str(i["id"])] = f'➡ {i["name"]}'
                                auth_users[user]["IDsRoom"].append(str(i["id"]))

                        text = ""
                        for index, word in finalmsg.items():
                            text = text + f"{index} {word}" + "\n"
                        finalMsgLast = finalMsgLast + "\n" + "".join(text)

                        for i in range(0, len(finalMsgLast), 4096):
                            bot_msg = bot.send_message(message.chat.id,
                                                       "<b>☑️| Записано!</b>\nВыберите помещение:\n" + finalMsgLast[
                                                                                                       i:i + 4096],
                                                       parse_mode="html")
                            auth_users[user]["lastbotmsg"] = bot_msg.message_id

                        auth_users[user]["StepOpros"] = 3
                    else:
                        bot.send_message(user, "<b>🔸| Указанного айди нет в списке.</b>", parse_mode="html")

                elif auth_users[user]["StepOpros"] == 3:
                    if message.text in auth_users[user]["IDsRoom"]:
                        auth_users[user]['CreateParams']['roomId'] = message.text

                        bot_msg = bot.send_message(user, "<b>☑️| Записано!</b>\nВведите <b>дату и время</b> начала:\n",
                                                   parse_mode="html")
                        auth_users[user]["lastbotmsg"] = bot_msg.message_id
                        auth_users[user]["StepOpros"] = 4
                    else:
                        bot.send_message(user, "<b>🔸| Указанного айди нет в списке.</b>", parse_mode="html")
                elif auth_users[user]["StepOpros"] == 4:
                    try:
                        sep = "."
                        if len(message.text.split(".")) == 3 or len(message.text.split("-")) == 3:
                            if (len(message.text.split(".")[0]) == 2 and len(message.text.split(".")[1]) == 2 and len(
                                    message.text.split(".")[2].split()[0]) == 4) or (
                                    len(message.text.split("-")[0]) == 2 and len(message.text.split("-")[1]) == 2 and len(
                                message.text.split("-")[2].split()[0]) == 4):
                                if "-" in message.text:
                                    sep = "-"
                                elif "-" in message.text and "." in message.text:
                                    print("Except!")

                                try:
                                    if len(message.text.split()) == 2:
                                        if int(message.text.split(sep)[0]) < 32 and int(
                                                message.text.split(sep)[1]) < 13 and int(
                                                message.text.split(sep)[2].split()[0]) <= datetime.now().year:
                                            auth_users[user]['CreateParams'][
                                                'startedAt'] = f"{message.text.split(sep)[2].split()[0]}-{message.text.split(sep)[1]}-{message.text.split(sep)[0]}T{message.text.split()[1].split(':')[0]}:{message.text.split()[1].split(':')[1]}:00"
                                            bot_msg = bot.send_message(user,
                                                                       "<b>☑️| Записано!</b>\nУкажите продолжительность ВКС. <i>(в минутах)</i>:\n",
                                                                       parse_mode="html")
                                            auth_users[user]["lastbotmsg"] = bot_msg.message_id
                                            auth_users[user]["StepOpros"] = 5
                                        else:
                                            bot.send_message(user, "<b>🔸| Введенной даты не существует!</b>",
                                                             parse_mode="html")

                                    else:
                                        bot.send_message(user,
                                                         f"<b>🔸|Ошибка!</b> Размер сообщения <b>меньше ожидаемого</b>. <i>(Ожидание: 2, Получено: {len(message.text)})</i>\n",
                                                         parse_mode="html")

                                except:
                                    tb.print_exc()

                                    bot.send_message(user,
                                                     "🔸|<b>Неверно</b>! Дата введена <b>не по формату</b>! Попробуйте ещё раз.",
                                                     parse_mode="html")

                            else:
                                bot.send_message(user, "<b>🔸| Введенной даты не существует!</b>", parse_mode="html")

                        else:

                            bot.send_message(user,
                                             "🔸|<b>Неверно</b>! Дата введена <b>не по формату</b>! Попробуйте ещё раз.",
                                             parse_mode="html")

                    except:
                        bot.send_message(user,
                                         "🔸| Произошла <b>внутренняя ошибка</b>. Убедитесь, что в <b>указанной дате</b> нет <b>специальных символов</b> и <b>букв</b> и попробуйте ещё раз!",
                                         parse_mode="html")

                elif auth_users[user]["StepOpros"] == 5:
                    if str(message.text).isdigit():
                        if int(message.text) % 15 == 0:
                            auth_users[user]['CreateParams']['duration'] = message.text
                            bot_msg = bot.send_message(user,
                                                       "<b>☑️| Записано!</b>\nУкажите участников (e-mail адреса через запятую):\n",
                                                       parse_mode="html")
                            auth_users[user]["lastbotmsg"] = bot_msg.message_id
                            auth_users[user]["StepOpros"] = 6
                        else:
                            bot.send_message(user, "<b>🔸|Ошибка!</b>\nЧисло должно быть <b>кратно 15</b>.\n",
                                             parse_mode="html")
                    else:
                        bot.send_message(user, "<b>🔸|Ошибка!\nВведите числовое значение.</b>",
                                         parse_mode="html")

                elif auth_users[user]["StepOpros"] == 6:
                    try:
                        if "@" in message.text and "." in message.text.split("@")[1] and len(message.text.split(",")) >= 2:

                            with requests.Session() as session:
                                # Устанавливаем заголовки для всех запросов через сессию
                                session.headers.update(headers)

                                # Обработка email-ов
                                for email in message.text.split(","):

                                    # Параметры запроса
                                    params2 = {
                                        "email": email.strip(),
                                        "timestamp": time.time()
                                    }

                                    print("Email: " + email.strip())

                                    # Выполняем запрос с использованием сессии
                                    response_users = session.get("https://test.vcc.uriit.ru/api/users", params=params2)

                                    # Обрабатываем ответ
                                    if response_users.status_code == 200:
                                        for i in response_users.json()["data"]:
                                            auth_users[user]['CreateParams']['participants'].append(
                                                {
                                                    "id": i["id"],
                                                    "roleIds": i["roleIds"],
                                                    "departmentId": i["departmentId"],
                                                    "lastName": i["lastName"],
                                                    "firstName": i["firstName"],
                                                    "middleName": i["middleName"],
                                                    "email": i["email"]
                                                }
                                            )
                                    else:
                                        print("Ошибка!!!")
                            pp(auth_users[user]['CreateParams']['participants'])

                            emails = auth_users[user]['CreateParams']['participants']

                            for text in emails:
                                auth_users[user]['CreateParams']['participantsEmails'].append(text["email"])

                            bot_msg = bot.send_message(user,
                                                       "<b>☑️| Записано!</b>\nУкажите максимальное количество участников:\n",
                                                       parse_mode="html")
                            auth_users[user]["lastbotmsg"] = bot_msg.message_id
                            auth_users[user]["StepOpros"] = 7
                        else:
                            bot.send_message(user,
                                             "<b>🔸|Ошибка!</b>\nНекорректно введена почта, либо же их количество недостаточно.\n",
                                             parse_mode="html")
                    except:
                        tb.print_exc()
                        bot.send_message(user,
                                         "<b>🔸|Ошибка!</b>\nНекорректно введена почта, либо же их количество недостаточно.\n",
                                         parse_mode="html")

                elif auth_users[user]["StepOpros"] == 7:

                    if str(message.text).isdigit():
                        if int(message.text) <= 100:
                            auth_users[user]['CreateParams']['participantsCount'] = message.text
                            bot_msg = bot.send_message(user, "<b>☑️| Записано!</b>\nВыберите средство проведения:\n",
                                                       parse_mode="html", reply_markup=addBackendButtons())
                            auth_users[user]["lastbotmsg"] = bot_msg.message_id
                            auth_users[user]["StepOpros"] = 8
                        else:
                            bot.send_message(user,
                                             "<b>🔸|Ошибка!</b>\nКоличество участников <b>не может превышать сотни</b>.\n",
                                             parse_mode="html")
                    else:
                        bot.send_message(user, "|Ошибка!\nВведите числовое значение.</b>\n",
                                         parse_mode="html")
                elif auth_users[user]["StepOpros"] == 8:
                    if message.text.lower() in ["cisco", "permanentroom", "external", "vinteo"]:
                        auth_users[user]["StepOpros"] = 9
                        auth_users[user]['CreateParams']['backend'] = message.text.lower()

                        response_getBuildName = requests.get(
                            f"https://test.vcc.uriit.ru/api/catalogs/buildings/{auth_users[user]['CreateParams']['buildId']}",
                            headers=headers)
                        response_getRoomName = requests.get(
                            f"https://test.vcc.uriit.ru/api/catalogs/rooms/{auth_users[user]['CreateParams']['roomId']}",
                            headers=headers)

                        bot.send_message(message.chat.id,
                                         "<b>┏━━━━━━━━━━━━━━━┓\n┃ Параметры Создания ВКС📩\n┗━━━━━━━━━━━━━━━┛</b>\n"
                                         f"🗒<b>Название</b>: {auth_users[user]['CreateParams']['name']}\n"
                                         f"🏢<b>Место проведения</b>: {response_getBuildName.json()['name']}\n"
                                         f"🏠<b>Помещение</b>: {response_getRoomName.json()['name']}\n"
                                         f"🗓<b>Дата и время начала</b>: {auth_users[user]['CreateParams']['startedAt']}\n"
                                         f"🕑<b>Продолжительность</b>: {auth_users[user]['CreateParams']['duration']} мин.\n"
                                         f"👥<b>Участники</b>: " + "\n- " + '\n- '.join(
                                             auth_users[user]['CreateParams']['participantsEmails']) +
                                         f"\n✋<b>Максимальное количество участников</b>: {auth_users[user]['CreateParams']['participantsCount']}\n"
                                         f"ℹ️<b>Средство проведения</b>: {auth_users[user]['CreateParams']['backend']}",

                                         parse_mode="html", reply_markup=addCreateButtons())
                    else:
                        bot.send_message(user, "<b>🔸| Воспользуйтесь клавиатурой!</b>", parse_mode="html",
                                         reply_markup=addBackendButtons())


                elif auth_users[user]["StepOpros"] == 9:
                    auth_users[user]["StepOpros"] = 0
                    auth_users[user]["CreateParams"] = {
                        "name": None,
                        "buildId": None,  # Айди здания, а не комнаты!!!
                        "roomId": None,
                        "startedAt": None,
                        "duration": None,
                        "participants": list(dict()),
                        "participantsEmails": list(),
                        "participantsCount": None,
                        "backend": None

                    }
                    bot.send_message(message.chat.id, "<b>🔸| Текущий запрос отменен.</b>\nВозвращаюсь в главное меню.",
                                     reply_markup=addMainButtons(user), parse_mode="html")
                    bot.register_next_step_handler(message, clickButton)
                if auth_users[user]["StepOpros"] != 0:
                    bot.register_next_step_handler(message, createVKSOpros)
            else:
                if auth_users[user]["StepOpros"] == 1:

                    if len(message.text) > 3:
                        auth_users[user]['CreateParams']['name'] = message.text

                        auth_users[user]['CreateParams']['roomId'] = message.text

                        bot_msg = bot.send_message(user, "<b>☑️| Записано!</b>\nВведите <b>дату и время</b> начала:\n",
                                                   parse_mode="html")
                        auth_users[user]["lastbotmsg"] = bot_msg.message_id
                        auth_users[user]["StepOpros"] = 2
                    else:
                        bot.send_message(message.chat.id,
                                         "🔸| <b>Название ВКС</b> не может быть <b>меньше 3-х символов</b>!",
                                         parse_mode="html")

                elif auth_users[user]["StepOpros"] == 2:
                    try:
                        sep = "."
                        if len(message.text.split(".")) == 3 or len(message.text.split("-")) == 3:
                            if (len(message.text.split(".")[0]) == 2 and len(message.text.split(".")[1]) == 2 and len(
                                    message.text.split(".")[2].split()[0]) == 4) or (
                                    len(message.text.split("-")[0]) == 2 and len(message.text.split("-")[1]) == 2 and len(
                                message.text.split("-")[2].split()[0]) == 4):
                                if "-" in message.text:
                                    sep = "-"
                                elif "-" in message.text and "." in message.text:
                                    print("Except!")

                                try:
                                    if len(message.text.split()) == 2:
                                        if int(message.text.split(sep)[0]) < 32 and int(
                                                message.text.split(sep)[1]) < 13 and int(
                                            message.text.split(sep)[2].split()[0]) <= datetime.now().year:
                                            auth_users[user]['CreateParams'][
                                                'startedAt'] = f"{message.text.split(sep)[2].split()[0]}-{message.text.split(sep)[1]}-{message.text.split(sep)[0]}T{message.text.split()[1].split(':')[0]}:{message.text.split()[1].split(':')[1]}:00"
                                            bot_msg = bot.send_message(user,
                                                                       "<b>☑️| Записано!</b>\nУкажите продолжительность ВКС. <i>(в минутах)</i>:\n",
                                                                       parse_mode="html")
                                            auth_users[user]["lastbotmsg"] = bot_msg.message_id
                                            auth_users[user]["StepOpros"] = 3
                                        else:
                                            bot.send_message(user, "<b>🔸| Введенной даты не существует!</b>",
                                                             parse_mode="html")

                                    else:
                                        bot.send_message(user,
                                                         f"<b>🔸|Ошибка!</b> Размер сообщения <b>меньше ожидаемого</b>. <i>(Ожидание: 2, Получено: {len(message.text)})</i>\n",
                                                         parse_mode="html")

                                except:
                                    tb.print_exc()

                                    bot.send_message(user,
                                                     "🔸|<b>Неверно</b>! Дата введена <b>не по формату</b>! Попробуйте ещё раз.",
                                                     parse_mode="html")

                            else:
                                bot.send_message(user, "<b>🔸| Введенной даты не существует!</b>", parse_mode="html")

                        else:

                            bot.send_message(user,
                                             "🔸|<b>Неверно</b>! Дата введена <b>не по формату</b>! Попробуйте ещё раз.",
                                             parse_mode="html")

                    except:
                        bot.send_message(user,
                                         "🔸| Произошла <b>внутренняя ошибка</b>. Убедитесь, что в <b>указанной дате</b> нет <b>специальных символов</b> и <b>букв</b> и попробуйте ещё раз!",
                                         parse_mode="html")
                elif auth_users[user]["StepOpros"] == 3:
                    if str(message.text).isdigit():
                        if int(message.text) % 15 == 0:
                            auth_users[user]['CreateParams']['duration'] = message.text
                            bot_msg = bot.send_message(user,
                                                       "<b>☑️| Записано!</b>\nУкажите участников (e-mail адреса через запятую):\n",
                                                       parse_mode="html")
                            auth_users[user]["lastbotmsg"] = bot_msg.message_id
                            auth_users[user]["StepOpros"] = 4
                        else:
                            bot.send_message(user, "<b>🔸|Ошибка!</b>\nЧисло должно быть <b>кратно 15</b>.\n",
                                             parse_mode="html")
                    else:
                        bot.send_message(user, "<b>🔸|Ошибка!\nВведите числовое значение.</b>",
                                         parse_mode="html")

                elif auth_users[user]["StepOpros"] == 4:
                    try:
                        if "@" in message.text and "." in message.text.split("@")[1] and len(message.text.split(",")) >= 2:

                            with requests.Session() as session:
                                # Устанавливаем заголовки для всех запросов через сессию
                                session.headers.update(headers)

                                # Обработка email-ов
                                for email in message.text.split(","):

                                    # Параметры запроса
                                    params2 = {
                                        "email": email.strip(),
                                        "timestamp": time.time()
                                    }

                                    # Выполняем запрос с использованием сессии
                                    response_users = session.get("https://test.vcc.uriit.ru/api/users", params=params2)

                                    # Обрабатываем ответ
                                    if response_users.status_code == 200:
                                        for i in response_users.json()["data"]:
                                            auth_users[user]['CreateParams']['participants'].append(
                                                {
                                                    "id": i["id"],
                                                    "roleIds": i["roleIds"],
                                                    "departmentId": i["departmentId"],
                                                    "lastName": i["lastName"],
                                                    "firstName": i["firstName"],
                                                    "middleName": i["middleName"],
                                                    "email": i["email"]
                                                }
                                            )
                                    else:
                                        print("Ошибка!!!")
                            pp(auth_users[user]['CreateParams']['participants'])

                            emails = auth_users[user]['CreateParams']['participants']

                            for text in emails:
                                auth_users[user]['CreateParams']['participantsEmails'].append(text["email"])

                            bot_msg = bot.send_message(user,
                                                       "<b>☑️| Записано!</b>\nУкажите максимальное количество участников:\n",
                                                       parse_mode="html")
                            auth_users[user]["lastbotmsg"] = bot_msg.message_id
                            auth_users[user]["StepOpros"] = 5
                        else:
                            bot.send_message(user,
                                             "<b>🔸|Ошибка!</b>\nНекорректно введена почта, либо же их количество недостаточно.\n",
                                             parse_mode="html")
                    except:
                        tb.print_exc()
                        bot.send_message(user,
                                         "<b>🔸|Ошибка!</b>\nНекорректно введена почта, либо же их количество недостаточно.\n",
                                         parse_mode="html")

                elif auth_users[user]["StepOpros"] == 5:

                    if str(message.text).isdigit():
                        if int(message.text) <= 100:
                            auth_users[user]['CreateParams']['participantsCount'] = message.text
                            bot_msg = bot.send_message(user, "<b>☑️| Записано!</b>\nВыберите средство проведения:\n",
                                                       parse_mode="html", reply_markup=addBackendButtons())
                            auth_users[user]["lastbotmsg"] = bot_msg.message_id
                            auth_users[user]["StepOpros"] = 6
                        else:
                            bot.send_message(user,
                                             "<b>🔸|Ошибка!</b>\nКоличество участников <b>не может превышать сотни</b>.\n",
                                             parse_mode="html")
                    else:
                        bot.send_message(user, "|Ошибка!\nВведите числовое значение.</b>\n",
                                         parse_mode="html")

                elif auth_users[user]["StepOpros"] == 6:
                    if message.text.lower() in ["cisco", "permanentroom", "external", "vinteo"]:
                        auth_users[user]["StepOpros"] = 7
                        auth_users[user]['CreateParams']['backend'] = message.text

                        bot.send_message(message.chat.id,
                                         "<b>┏━━━━━━━━━━━━━━━┓\n┃ Параметры Создания ВКС📩\n┗━━━━━━━━━━━━━━━┛</b>\n"
                                         f"🗒<b>Название</b>: {auth_users[user]['CreateParams']['name']}\n"
    
                                         f"🗓<b>Дата и время начала</b>: {auth_users[user]['CreateParams']['startedAt']}\n"
                                         f"🕑<b>Продолжительность</b>: {auth_users[user]['CreateParams']['duration']} мин.\n"
                                         f"👥<b>Участники</b>: " + "\n- " + '\n- '.join(
                                             auth_users[user]['CreateParams']['participantsEmails']) +
                                         f"\n✋<b>Максимальное количество участников</b>: {auth_users[user]['CreateParams']['participantsCount']}\n"
                                         f"ℹ️<b>Средство проведения</b>: {auth_users[user]['CreateParams']['backend']}",

                                         parse_mode="html", reply_markup=addCreateButtons())
                    else:
                        bot.send_message(user, "<b>🔸| Воспользуйтесь клавиатурой!</b>", parse_mode="html",
                                         reply_markup=addBackendButtons())

                elif auth_users[user]["StepOpros"] == 7:
                    auth_users[user]["StepOpros"] = 0
                    auth_users[user]["CreateParams"] = {
                        "name": None,
                        "buildId": None,  # Айди здания, а не комнаты!!!
                        "roomId": None,
                        "startedAt": None,
                        "duration": None,
                        "participants": list(dict()),
                        "participantsEmails": list(),
                        "participantsCount": None,
                        "backend": None

                    }
                    bot.send_message(message.chat.id, "<b>🔸| Текущий запрос отменен.</b>\nВозвращаюсь в главное меню.",
                                     reply_markup=addMainButtons(user), parse_mode="html")
                    bot.register_next_step_handler(message, clickButton)
                if auth_users[user]["StepOpros"] != 0:
                    bot.register_next_step_handler(message, createVKSOpros)
        else:
            bot.send_message(message.chat.id, "<b>🔸| Подождите немного перед использованием!</b>", parse_mode="html",
                             reply_markup=addMainButtons(user))
    except:
        print("Error")


def dateHandler(message):
    try:
        user = message.chat.id

        currentTime = time.time()
        if currentTime - auth_users[user]["lastmsgtime"] > 1:
            auth_users[user]["lastmsgtime"] = time.time()
            if message.text.lower() == "/cancel" or message.text.lower() == "/stop" or message.text.lower() == "стоп" or message.text.lower() == "хватит" or message.text.lower() == "отмена":
                sbros(user)
                bot.send_message(message.chat.id,
                                 "<b>🔸| Отменил все текущие действия</b>.\nВыберите то, что Вас интересует:",
                                 parse_mode="html", reply_markup=addMainButtons(user))
                bot.register_next_step_handler(message, clickButton)
            else:

                try:
                    sep = "."
                    if len(message.text.split(".")) == 3 or len(message.text.split("-")) == 3:
                        if (len(message.text.split(".")[0]) == 2 and len(message.text.split(".")[1]) == 2 and len(
                                message.text.split(".")[2]) == 4) or (
                                len(message.text.split("-")[0]) == 2 and len(message.text.split("-")[1]) == 2 and len(
                                message.text.split("-")[2]) == 4):
                            if "-" in message.text:
                                sep = "-"
                            elif "-" in message.text and "." in message.text:
                                if int(message.text.split(sep)[0]) < 32 and int(message.text.split(sep)[1]) < 13 and int(
                                        message.text.split(sep)[2]) <= datetime.now().year:

                                    if auth_users[user]["FirstDateBool"]:
                                        try:
                                            auth_users[user][
                                                "FirstDate"] = f'{message.text.split(".")[2]}-{message.text.split(".")[1]}-{message.text.split(".")[0]}'

                                            bot.send_message(message.chat.id,
                                                             f"<b>━━━━━━━━━━🌟━━━━━━━━━━</b>\n\n📅 Укажите <b>конец периода проведения</b> ВКС. \n\n🔎 Начало: <b>{auth_users[user]['FirstDate']}</b>\n🔍 Конец: <b>{auth_users[user]['LastDate']}</b> \n🕒 Пример: <i>07.11.2024</i>\n<b>━━━━━━━━━━✨━━━━━━━━━━</b>",
                                                             reply_markup=types.ReplyKeyboardRemove(True),
                                                             parse_mode="html")

                                            auth_users[user]["FirstDateBool"] = False
                                            bot.register_next_step_handler(message, dateHandler)
                                        except:
                                            try:
                                                auth_users[user][
                                                    "FirstDate"] = f'{message.text.split("-")[2]}-{message.text.split("-")[1]}-{message.text.split("-")[0]}'
                                                bot.send_message(message.chat.id,
                                                                 f"<b>━━━━━━━━━━🌟━━━━━━━━━━</b>\n\n📅 Укажите <b>конец периода проведения</b> ВКС. \n\n🔎 Начало: <b>{auth_users[user]['FirstDate']}</b>\n🔍 Конец: <b>{auth_users[user]['LastDate']}</b> \n🕒 Пример: <i>07.11.2024</i>\n<b>━━━━━━━━━━✨━━━━━━━━━━</b>",
                                                                 reply_markup=types.ReplyKeyboardRemove(True),
                                                                 parse_mode="html")

                                                auth_users[user]["FirstDateBool"] = False
                                                bot.register_next_step_handler(message, dateHandler)
                                            except:
                                                bot.send_message(user,
                                                                 "🔸| <b>Неверно</b>! Дата введена <b>не по формату</b>! Попробуйте ещё раз.",
                                                                 parse_mode="html")
                                                bot.register_next_step_handler(message, dateHandler)


                                    else:
                                        try:
                                            auth_users[user][
                                                "LastDate"] = f'{message.text.split(".")[2]}-{message.text.split(".")[1]}-{message.text.split(".")[0]}'
                                            auth_users[user]['FirstDate'].replace("-", ".")
                                            auth_users[user]['LastDate'].replace("-", ".")
                                            if datetime(int(auth_users[user]['FirstDate'].replace("-", ".").split(".")[0]),
                                                        int(auth_users[user]['FirstDate'].replace("-", ".").split(".")[1]),
                                                        int(auth_users[user]['FirstDate'].replace("-", ".").split(".")[
                                                                2])) > (
                                            datetime(int(auth_users[user]['LastDate'].replace("-", ".").split(".")[0]),
                                                     int(auth_users[user]['LastDate'].replace("-", ".").split(".")[1]),
                                                     int(auth_users[user]['LastDate'].replace("-", ".").split(".")[2]))):
                                                first, last = auth_users[user]['FirstDate'], auth_users[user]['LastDate']

                                                auth_users[user]['FirstDate'] = last
                                                auth_users[user]['LastDate'] = first

                                            button = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                            button.add("Верно")
                                            button.add("Неверно")

                                            bot.send_message(message.chat.id,
                                                             f"<b>━━━━━━━━━━🌟━━━━━━━━━━</b>\n\n📅 Проверьте <b>правильность</b> введённых данных: \n\n🔎 Начало: <b>{auth_users[user]['FirstDate']}</b>\n🔍 Конец: <b>{auth_users[user]['LastDate']}</b>\n<b>━━━━━━━━━━✨━━━━━━━━━━</b>",
                                                             reply_markup=button, parse_mode="html")
                                            bot.register_next_step_handler(message, receive)

                                        except:
                                            tb.print_exc()
                                            try:
                                                auth_users[user][
                                                    "LastDate"] = f'{message.text.split("-")[2]}-{message.text.split("-")[1]}-{message.text.split("-")[0]}'

                                                auth_users[user]['FirstDate'].replace(".", "-")
                                                auth_users[user]['LastDate'].replace(".", "-")
                                                if datetime(
                                                        int(auth_users[user]['FirstDate'].replace("-", ".").split("-")[0]),
                                                        int(auth_users[user]['FirstDate'].replace("-", ".").split("-")[1]),
                                                        int(auth_users[user]['FirstDate'].replace("-", ".").split("-")[
                                                                2])) > datetime(
                                                    int(auth_users[user]['LastDate'].replace("-", ".").split("-")[0]),
                                                    int(auth_users[user]['LastDate'].replace("-", ".").split("-")[1]),
                                                    int(auth_users[user]['LastDate'].replace("-", ".").split("-")[2])):
                                                    first, last = auth_users[user]['FirstDate'], auth_users[user][
                                                        'LastDate']

                                                    auth_users[user]['FirstDate'] = last
                                                    auth_users[user]['LastDate'] = first

                                                button = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                                button.add("Верно")
                                                button.add("Неверно")

                                                bot.send_message(message.chat.id,
                                                                 f"<b>━━━━━━━━━━🌟━━━━━━━━━━</b>\n\n📅 Проверьте <b>правильность</b> введённых данных: \n\n🔎 Начало: <b>{auth_users[user]['FirstDate']}</b>\n🔍 Конец: <b>{auth_users[user]['LastDate']}</b>\n<b>━━━━━━━━━━✨━━━━━━━━━━</b>",
                                                                 reply_markup=button, parse_mode="html")
                                                bot.register_next_step_handler(message, receive)
                                            except:

                                                bot.send_message(user,
                                                                 "❌<b>Неверно</b>! Дата введена <b>не по формату</b>! Попробуйте ещё раз.",
                                                                 parse_mode="html")
                                                bot.register_next_step_handler(message, dateHandler)
                                else:
                                    bot.send_message(user, "<b>🔸| Введенной даты не существует!</b>")
                                    bot.register_next_step_handler(message, dateHandler)
                        else:

                            bot.send_message(user,
                                             "🔸|<b>Неверно</b>! Дата введена <b>не по формату</b>! Попробуйте ещё раз.",
                                             parse_mode="html")
                            bot.register_next_step_handler(message, dateHandler)
                    else:

                        bot.send_message(user, "🔸|<b>Неверно</b>! Дата введена <b>не по формату</b>! Попробуйте ещё раз.",
                                         parse_mode="html")
                        bot.register_next_step_handler(message, dateHandler)
                except:
                    bot.send_message(user,
                                     "🔸| Произошла <b>внутренняя ошибка</b>. Убедитесь, что в <b>указанной дате</b> нет <b>специальных символов</b> и <b>букв</b> и попробуйте ещё раз!",
                                     parse_mode="html")
                    bot.register_next_step_handler(message, dateHandler)
        else:
            bot.send_message(message.chat.id, "<b>🔸| Подождите немного перед использованием!</b>", parse_mode="html",
                             )
    except:
        print("Error")


def receive(message):
    try:
        user = message.chat.id

        currentTime = time.time()
        if currentTime - auth_users[user]["lastmsgtime"] > 1:
            auth_users[user]["lastmsgtime"] = time.time()
            if message.text == "Верно":
                bot.send_message(message.chat.id,
                                 f"✔️| <b>Информация принята</b>! \n📅| Записанная дата для фильтрации: \n <b>➤| Начало</b>:<i> {auth_users[user]['FirstDate']}</i>\n <b>➤| Конец</b>: <i>{auth_users[user]['LastDate']}</i>",
                                 reply_markup=addMainButtons(user), parse_mode="html")
                auth_users[user]["FirstParams"]["fromDatetime"] = f"{auth_users[user]['FirstDate']}T00:00:00.00"
                auth_users[user]["FirstParams"]["toDatetime"] = f"{auth_users[user]['LastDate']}T23:59:59.00"
                bot.register_next_step_handler(message, clickButton)

                ## Запрос к API
            elif message.text == "Неверно":
                bot.send_message(message.chat.id, "➤| Информация <b>очищена</b>! Возвращаю Вас в <b>главное меню</b>.",
                                 reply_markup=addMainButtons(user),
                                 parse_mode="html")
                sbros_Date(user)
                bot.register_next_step_handler(message, clickButton)
        else:
            bot.send_message(message.chat.id, "<b>🔸| Подождите немного перед использованием!</b>", parse_mode="html")
    except:
        print("Error")


@bot.message_handler(commands=['auth', 'login', 'логин'])
def log_user(message):
    try:
        user = message.chat.id
        auth = last_user in auth_users_list

        if auth:
            bot.send_message(message.chat.id, "<b>🔸| Вы уже авторизованы!</b>", parse_mode="html")
        else:
            auth_split = message.any_text.split()
            if len(auth_split) != 3:
                bot.send_message(message.chat.id,
                                 "🔸| <b>Неверно</b>!\nАвторизуйтесь по форме: <b>/login</b> <i>\"email\" \"пароль\"</i>",
                                 parse_mode="html")
            else:
                text_login = message.any_text.split()[1]
                text_password = message.any_text.split()[2]

                data = {
                    "login": f"{text_login}",
                    "password": f"{text_password}",
                    "fingerprint": {
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
                        "webdriver": "",
                        "language": "ru",
                        "colorDepth": 24,
                        "deviceMemory": 8,
                        "hardwareConcurrency": 12,
                        "screenHeight": 1920,
                        "screenWidth": 1080,
                        "timezoneOffset": -180,
                        "timezone": "Europe/Moscow",
                        "localStorage": True,
                        "indexedDb": True,
                        "openDatabase": True,
                        "adBlock": True,
                        "audio": "124.04347527516074",
                        "hasLiedOs": None,
                        "hasLiedBrowser": None,
                        "hasLiedLanguages": None,
                        "hasLiedResolution": None,
                        "hasTouchSupport": None
                    }
                }

                response = requests.post("https://test.vcc.uriit.ru/api/auth/login", json=data)
                print("Successfully auth!")

                if response:
                    auth_users_list.append(user)
                    auth_users[user] = dict()
                    auth_users[user]["login"] = text_login
                    auth_users[user]["password"] = text_password
                    auth_users[user]["Authorization"] = True
                    auth_setParams(user)
                    bot.send_message(message.chat.id,
                                     f"✔️ Авторизация прошла <b>успешно</b>!\n👋Приветствую тебя, <b>{text_login}</b>. Выбери то, что тебя интересует:",
                                     parse_mode="html", reply_markup=addMainButtons(user))
                    bot.register_next_step_handler(message, clickButton)
                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



                else:
                    bot.send_message(message.chat.id, "🔸| Введены <b>неверные данные</b> от учетной записи!",
                                     parse_mode="html")
    except:
        print("Error")


@bot.message_handler()
def info(message):
    try:
        global last_user
        # Задание айди пользователя в глобальную переменную
        last_user = message.chat.id
        auth = last_user in auth_users_list

        user = message.chat.id

        if not auth:
            bot.send_message(message.chat.id,
                             f"👋 Приветствую, <b>{message.from_user.first_name}</b>! Чтобы <b>пользоваться функционалом</b> этого бота требуется <b>авторизация</b>.\n🔔Авторизоваться можно, используя команду <b>/login</b> <i>имя_пользователя пароль_пользователя</i>.",
                             parse_mode="html")
        else:
            currentTime = time.time()
            if currentTime - auth_users[user]["lastmsgtime"] > 1:
                auth_users[user]["lastmsgtime"] = time.time()
                if auth_users[user]["ToContinue"] and "Продолжить" in message.text:
                    bot.send_message(user, "| <b>➤| Перенаправляю Вас в меню поиска</b>...", parse_mode="html",
                                     reply_markup=types.ReplyKeyboardRemove(True))
                    openButtonVKS(message)
                    auth_users[user]["ToContinue"] = False
                elif auth_users[user]["ToContinue"] and "Меню выбора дат" in message.text:
                    bot.send_message(user, "| <b>➤| Перенаправляю Вас в меню выбора дат</b>...", parse_mode="html",
                                     reply_markup=types.ReplyKeyboardRemove(True))
                    menuDates(user, message.chat.id, message)
                    auth_users[user]["ToContinue"] = False
                elif message.text == "Состояние":
                    auth_users[user]['Filter'] = "Состояние"
                    bot.send_message(message.chat.id, "➤| Выберите желаемое <b>состояние:</b>",
                                     reply_markup=addFilterButtons(),
                                     parse_mode="html")
                elif message.text == "Наименование":
                    auth_users[user]['Filter'] = "Наименование"
                    auth_users[user]['ToNameFilter'] = True
                    bot.send_message(message.chat.id, "➤| Введите <b>название ВКС </b>для поиска.",
                                     parse_mode="html")
                elif message.text == "Приоритет":
                    auth_users[user]['Filter'] = "Приоритет"
                    auth_users[user]['ToPriorityFilter'] = True
                    bot.send_message(message.chat.id, "➤| Выберите желаемый <b>приоритет</b>:",
                                     reply_markup=addPriorityButtons(),
                                     parse_mode="html")
                elif message.text == "Департамент":
                    auth_users[user]['Filter'] = "Департамент"

                    auth_users[user]['ToNameDep'] = True
                    bot.send_message(message.chat.id,
                                     "➤| Введите <b>название департамента</b> для начала поиска.\nℹ️Примечание: <i> Вы можете указать лишь часть названия.</i>",
                                     parse_mode="html")
                elif message.text == "Организатор":
                    auth_users[user]['Filter'] = "Организатор"
                    auth_users[user]['ToNameOrg'] = True
                    bot.send_message(message.chat.id, "➤| Введите <b>имя/фамилию организатора</b> для начала поиска.",
                                     parse_mode="html")

                # Фильтр для состояния
                elif auth_users[user]['Filter'] == "Состояние":
                    if message.text == "Забронированные":
                        auth_users[user]['Status'] = "Забронированные"
                        auth_users[user]["FirstParams"]["state"] = "booked"
                        bot.send_message(message.chat.id, "➤| Состояние изменено на <b>\"Забронированные\"</b>",
                                         reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                        openButtonVKS(message)
                    elif message.text == "Начатые":
                        auth_users[user]['Status'] = "Начатые"

                        auth_users[user]["FirstParams"]["state"] = "started"
                        bot.send_message(message.chat.id, "➤| Состояние изменено на <b>\"Начатые\"</b>",
                                         reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                        openButtonVKS(message)
                    elif message.text == "Законченные":
                        auth_users[user]['Status'] = "Законченные"

                        auth_users[user]["FirstParams"]["state"] = "ended"
                        bot.send_message(message.chat.id, "➤| Состояние изменено на <b>\"Законченные\"</b>",
                                         reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                        openButtonVKS(message)
                    elif message.text == "Отмененные":
                        auth_users[user]['Status'] = "Отмененные"
                        auth_users[user]["FirstParams"]["state"] = "cancelled"
                        bot.send_message(message.chat.id, "➤| Состояние изменено на <b>\"Отмененные\"</b>",
                                         reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                        openButtonVKS(message)

                    # Фильтр для наименования
                elif auth_users[user]['Filter'] == "Наименование":
                    if auth_users[user]['ToNameFilter']:
                        auth_users[user]["FirstParams"]["filter"] = message.text
                        bot.send_message(message.chat.id, f"Название <b>{message.text}</b> записано.",
                                         reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                        openButtonVKS(message)
                        auth_users[user]['ToNameFilter'] = False
                    else:
                        bot.send_message(message.chat.id, f"Название <b>уже записано.</b>",
                                         reply_markup=addFilterButtonsMAIN(), parse_mode="html")

                # Фильтр для приоритета
                elif auth_users[user]['Filter'] == "Приоритет":
                    if auth_users[user]['ToPriorityFilter']:
                        if "низкий" in message.text.lower() or "средний" in message.text.lower() or "высокий" in message.text.lower():
                            if message.text == "Низкий":
                                auth_users[user]["FirstParams"]["priority"] = 3
                            elif message.text == "Средний":
                                auth_users[user]["FirstParams"]["priority"] = 2
                            elif message.text == "Высокий":
                                auth_users[user]["FirstParams"]["priority"] = 1
                            bot.send_message(message.chat.id, f"Выбранный приоритет: <b>{message.text}</b>.",
                                             reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                            openButtonVKS(message)
                            auth_users[user]['ToPriorityFilter'] = False
                        else:
                            bot.send_message(message.chat.id, f"<b>🔸| Воспользуйтесь клавиатурой!</b>",
                                             reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                    else:
                        bot.send_message(message.chat.id, f"Приоритет <b>уже задан.</b>",
                                         reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                # Фильтр для департамента
                elif auth_users[user]['Filter'] == "Департамент":
                    if auth_users[user]['ToNameDep']:
                        auth_users[user]["DepartParams"]["name"] = message.text
                        headers = {
                            "Authorization": f"Bearer {authorization(user)}"
                        }
                        # Запрос для получения айди департамента по названию
                        pp(f'Susfd: {auth_users[user]["DepartParams"]["name"]}')
                        response_buildroom = requests.get(f"https://test.vcc.uriit.ru/api/catalogs/departments",
                                                          headers=headers, params=auth_users[user]["DepartParams"])
                        # Получение айди
                        pp(f'Дата: {response_buildroom.json()["data"]}')
                        if response_buildroom.json()["data"]:

                            auth_users[user]["FirstParams"]["departmentId"] = response_buildroom.json()["data"][0]["id"]
                            bot.send_message(message.chat.id, f"Департамент <b>{message.text}</b> записан.",
                                             reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                            auth_users[user]['ToNameDep'] = False
                        else:
                            bot.send_message(message.chat.id, f"🔸| Указанного департамента <b>не существует</b>.",
                                             reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                            auth_users[user]['ToNameDep'] = False
                        # Фильтр для организатора
                elif auth_users[user]['Filter'] == "Организатор":
                    if auth_users[user]['ToNameOrg']:
                        auth_users[user]["DepartParams"]["name"] = message.text
                        headers = {
                            "Authorization": f"Bearer {authorization(user)}"
                        }
                        # Запрос для получения айди организатора по имени
                        response_buildroom = requests.get(f"https://test.vcc.uriit.ru/api/users",
                                                          headers=headers, params=auth_users[user]["DepartParams"])
                        # Получение айди
                        if response_buildroom:
                            if response_buildroom.json()["data"]:

                                auth_users[user]["FirstParams"]["userId"] = response_buildroom.json()["data"][0]["id"]
                                bot.send_message(message.chat.id, f"Организатор <b>{message.text}</b> записан.",
                                                 reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                                auth_users[user]['ToNameOrg'] = False
                            else:
                                bot.send_message(message.chat.id, f"Указанного организатора <b>не существует</b>.",
                                                 reply_markup=addFilterButtonsMAIN(), parse_mode="html")
                                auth_users[user]['ToNameOrg'] = False
                                openButtonVKS(message)
                        else:
                            bot.send_message(message.chat.id,
                                             f"Произошла<b> внутренняя ошибка! {response_buildroom.status_code}</b>.")
                            openButtonVKS(message)

                elif message.text == "/exit":
                    if auth:
                        bot.send_message(message.chat.id, "<b>🔸| Вы вышли из учетной записи.</b>", parse_mode="html")
                        auth_users_list.remove(user)
                    else:
                        bot.send_message(message.chat.id, "<b>🔸| Ошибка! Вы не авторизованы.</b>", parse_mode="html")
                else:
                    print("Сброс!")
                    sbros(user)
                    bot.send_message(message.chat.id, "➤| <b>Ничего не понял</b>! Выберите то, что Вас <b>интересует</b>:",
                                     reply_markup=addMainButtons(user), parse_mode="html")
                    bot.register_next_step_handler(message, clickButton)
            else:
                bot.send_message(message.chat.id, "<b>🔸| Подождите немного перед использованием!</b>", parse_mode="html",
                                 )
    except:
        print("Error")


@bot.callback_query_handler(func=lambda call: True)
def handlerCallbacks(call):
    try:
        user = call.message.chat.id
        if call.data == "OnBuild" and not auth_users[user]["BuildBool"]:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="👋Привет! Для <b>создания ВКС</b> понадобится следующая информация:\n"
                                       "<b>- Название.</b>\n"
                                       "<b>- Место проведения.</b>\n"
                                       "<b>- Помещение.</b>\n"
                                       "<b>- Дата и время начала.</b>\n"
                                       "<b>- Продолжительность.</b>\n"
                                       "<b>- Адреса участников.</b>\n"
                                       "<b>- Максимальное количество участников.</b>\n"
                                       "<b>- Средство проведения.</b>",

                                  parse_mode="html", reply_markup=addSettingsButton(user))


        elif call.data == "OnBuild":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="👋Привет! Для <b>создания ВКС</b> понадобится следующая информация:\n"
                                       "<b>- Название.</b>\n"
                                       "<b>- Дата и время начала.</b>\n"
                                       "<b>- Продолжительность.</b>\n"
                                       "<b>- Адреса участников.</b>\n"
                                       "<b>- Максимальное количество участников.</b>\n"
                                       "<b>- Средство проведения.</b>", parse_mode="html",
                                  reply_markup=addSettingsButton(user))

        if call.data == "CreateConf":
            try:
                headers = {
                    "Authorization": f"Bearer {authorization(user)}"
                }

                response_acc = requests.get("https://test.vcc.uriit.ru/api/account/user-info", headers=headers)

                print(auth_users[user]['CreateParams']['participants'])
                if auth_users[user]["BuildBool"]:
                    data = {

                        "id": None,
                        "name": f"{auth_users[user]['CreateParams']['name']}",
                        "roomId": int(auth_users[user]['CreateParams']['roomId']),
                        "comment": "",
                        "participantsCount": f"{auth_users[user]['CreateParams']['participantsCount']}",
                        "ciscoSettings": {
                            "isMicrophoneOn": True,
                            "isVideoOn": True,
                            "isWaitingRoomEnabled": False,
                            "needVideoRecording": True
                        },
                        "vinteoSettings": {
                            "needVideoRecording": True
                        },
                        "externalSettings": {
                            "externalUrl": "",
                            "permanentRoomId": None
                        },
                        "state": "booked",
                        "backend": f"{auth_users[user]['CreateParams']['backend'].lower()}",
                        "sendNotificationsAt": 0,
                        "startedAt": f"{auth_users[user]['CreateParams']['startedAt']}",
                        "endedAt": None,
                        "organizedBy": {
                            "id": int(response_acc.json()["id"])
                        },
                        "isGovernorPresents": False,
                        "duration": int(auth_users[user]['CreateParams']['duration']),
                        "isNotifyAccepted": False,
                        "isVirtual": False,
                        "recurrence": None,
                        "participants": auth_users[user]['CreateParams']['participants'],
                        "attachments": [],
                        "groups": []
                    }
                else:
                    data = {

                        "id": None,
                        "name": f"{auth_users[user]['CreateParams']['name']}",
                        "comment": "",
                        "participantsCount": f"{auth_users[user]['CreateParams']['participantsCount']}",
                        "ciscoSettings": {
                            "isMicrophoneOn": True,
                            "isVideoOn": True,
                            "isWaitingRoomEnabled": False,
                            "needVideoRecording": True
                        },
                        "vinteoSettings": {
                            "needVideoRecording": True
                        },
                        "externalSettings": {
                            "externalUrl": "",
                            "permanentRoomId": None
                        },
                        "state": "booked",
                        "backend": f"{auth_users[user]['CreateParams']['backend'].lower()}",
                        "sendNotificationsAt": 0,
                        "startedAt": f"{auth_users[user]['CreateParams']['startedAt']}",
                        "endedAt": None,
                        "organizedBy": {
                            "id": int(response_acc.json()["id"])
                        },
                        "isGovernorPresents": False,
                        "duration": int(auth_users[user]['CreateParams']['duration']),
                        "isNotifyAccepted": False,
                        "isVirtual": False,
                        "recurrence": None,
                        "participants": auth_users[user]['CreateParams']['participants'],
                        "attachments": [],
                        "groups": []
                    }

                pp(("data:", data))

                response_post = requests.post(f"https://test.vcc.uriit.ru/api/meetings", headers=headers, json=data)

                try:
                    if response_post:
                        pp(response_post.json())
                        bot.send_message(call.message.chat.id,
                                         f"<b>Конференция успешно создана</b>!\nСсылка для подключения: {response_post.json()['permalink']}",
                                         parse_mode="html", reply_markup=addMainButtons(user))
                        auth_users[user]["StepOpros"] = 0
                        bot.register_next_step_handler(call.message, clickButton)
                    else:
                        pp(response_post.text)
                        bot.send_message(call.message.chat.id,
                                         f"🔸| <b>Ошибка создания ВКС. Попробуйте снова спустя время.</b>",
                                         reply_markup=addMainButtons(user), parse_mode="html")
                        auth_users[user]["StepOpros"] = 0
                        bot.register_next_step_handler(call.message, clickButton)
                except:
                    pp(response_post)
                    tb.print_exc()
            except:
                tb.print_exc()

        if call.data == "Cancel":
            if auth_users[user]["StepOpros"] == 9:
                auth_users[user]["StepOpros"] = 0
                auth_users[user]["CreateParams"] = {
                    "name": None,
                    "buildId": None,  # Айди здания, а не комнаты!!!
                    "roomId": None,
                    "startedAt": None,
                    "duration": None,
                    "participants": list(dict()),
                    "participantsEmails": list(),
                    "participantsCount": None,
                    "backend": None

                }
                bot.send_message(call.message.chat.id, "<b>🔸| Текущий запрос отменен. Возвращаюсь в главное меню.</b>",
                                 reply_markup=addMainButtons(user), parse_mode="html")
                bot.register_next_step_handler(call.message, clickButton)
            else:
                bot.send_message(call.message.chat.id, "Сейчас запросов нет.")

        if call.data == "ChangeFilter":
            bot.send_message(user, "➤| Выберите <b>любой желаемый фильтр</b>.", parse_mode="html",
                             reply_markup=addFilterButtonsMAIN())
        if call.data == "Search":
            user = call.message.chat.id
            auth = last_user in auth_users_list
            if auth:
                if auth_users[user]["FirstDate"] != "Не указано":
                    if auth_users[user]['Filter'] != "Не выбрано":
                        bot.send_message(user, "<b>⏳| Начинаю поиск по заданным фильтрам</b>...",
                                         reply_markup=types.ReplyKeyboardRemove(True), parse_mode="html")

                    else:
                        bot.send_message(user, "<b>⏳| Осуществляю поиск всех ВКС</b>...",
                                         reply_markup=types.ReplyKeyboardRemove(True), parse_mode="html")

                    headers = {
                        "Authorization": f"Bearer {authorization(user)}"
                    }

                    response_rooms = requests.get("https://test.vcc.uriit.ru/api/meetings", headers=headers,
                                                  params=auth_users[user]["FirstParams"])

                    if response_rooms:
                        finalMsgLast = ""
                        number = 1
                        for lst in response_rooms.json()["data"]:

                            # Имя ВКС
                            name = lst["name"]
                            # Айди комнаты
                            roomId = lst["id"]
                            # Дата и время начала
                            createdAt = lst["createdAt"]
                            # Продолжительность
                            dur = lst["duration"]
                            if dur >= 60:
                                dur = str(lst["duration"] // 60) + " ч."
                            else:
                                dur = str(lst["duration"]) + " мин."

                            params = {
                                "organizedUser": {
                                    "firstname": "Никита",
                                    "lastName": "Платинов"
                                }
                            }

                            response_idroom = requests.get(f"https://test.vcc.uriit.ru/api/meetings/{roomId}",
                                                           headers=headers)

                            # Место проведения
                            field = response_idroom.json()["room"]
                            if field:
                                field = response_idroom.json()["room"]["name"]
                            else:
                                field = "Отсутствует"
                            # Имя организатора
                            orgUser = f'{response_idroom.json()["organizedUser"]["firstName"]} {response_idroom.json()["organizedUser"]["lastName"]}'
                            # Список участников
                            participants = list()
                            for ls in response_idroom.json()["participants"]:
                                firstName, lastName = ls["firstName"], ls["lastName"]
                                participants.append(f"{firstName} {lastName}")
                            # Средство проведения
                            platform = response_idroom.json()["backend"]

                            finalMsg = {
                                "🗒<b>Название ВКС</b>:": f'"{name}"',
                                "🏢<b>Место проведения</b>:": f"{field}",
                                "🗓<b>Дата и время начала</b>:": f"{createdAt.split('T')[0]} {createdAt.split('T')[1].split(':')[0]}:{createdAt.split('T')[1].split(':')[1]}",
                                "🕑<b>Продолжительность</b>:": f"{dur}",
                                "👤<b>Организатор</b>:": f"{orgUser}",
                                "👥<b>Участники</b>:": "\n- <i>" + '\n- '.join(participants) + "</i>",
                                "ℹ️<b>Средство проведения</b>:": f"{platform}",
                            }

                            text = ""
                            for index, word in finalMsg.items():
                                text = text + f"{index} {word}" + "\n"
                            part = text
                            if len(finalMsgLast) + len(part) > 4096:
                                bot.send_message(call.message.chat.id,
                                                 f"<b>┏━━━━━━━━━━━━━━┓\n┃ Результаты поиска №{number}📩</b>\n┗━━━━━━━━━━━━━━┛\n📍Фильтрация: <b>{auth_users[user]['Filter']}</b>\n{finalMsgLast}",
                                                 parse_mode="html")
                                finalMsgLast = ""
                                number += 1
                            else:
                                finalMsgLast = finalMsgLast + "\n" + "".join(text)
                        if finalMsgLast:
                            bot.send_message(call.message.chat.id,
                                             f"<b>┏━━━━━━━━━━━━━━┓\n┃ Результаты поиска №{number}📩</b>\n┗━━━━━━━━━━━━━━┛\n📍Фильтрация: <b>{auth_users[user]['Filter']}</b>\n{finalMsgLast}",
                                             parse_mode="html")
                        else:
                            bot.send_message(user, "<b>🔸| По заданным параметрам ничего на найдено.</b>",
                                             parse_mode="html")
                        auth_users[user]['Filter'] = "Не выбрано"
                    else:
                        print(response_rooms.text, response_rooms)
                else:
                    bot.send_message(user,
                                     "🔸| Вы не можете <b>начать поиск</b> без указания <b>периода проведения</b>.",
                                     reply_markup=addMainButtons(user), parse_mode="html")
                    bot.register_next_step_handler(call.message, clickButton)

            else:
                bot.send_message(call.message.chat.id,
                                 f"Привет, {call.message.from_user.first_name}, для продолжения требуется авторизация.\n Воспользуйтесь командой /register для регистрации пользователя.\n Воспользуйтесь командой /login для авторизации пользователя.")
        if call.data == "FastToday":
            date = datetime.now().date()
            auth_users[user][
                "FirstDate"] = f'{date.year}-{date.month}-{date.day}'
            auth_users[user][
                "LastDate"] = f'{date.year}-{date.month}-{date.day}'

            auth_users[user]["FirstParams"]["fromDatetime"] = f"{auth_users[user]['FirstDate']}T00:00:00.00"
            auth_users[user]["FirstParams"]["toDatetime"] = f"{auth_users[user]['LastDate']}T23:59:59.00"

            bot.send_message(call.message.chat.id,
                             f"✔️| <b>Информация принята</b>! \n📅| Записанная дата для фильтрации: \n <b>➤| Начало</b>:<i> {auth_users[user]['FirstDate']}</i>\n <b>➤| Конец</b>: <i>{auth_users[user]['LastDate']}</i>",
                             reply_markup=addMainButtons(user), parse_mode="html")
            bot.clear_step_handler_by_chat_id(user)

            bot.register_next_step_handler(call.message, clickButton)
        if call.data == "FastWeek":
            date = datetime.now().date()
            date_week = datetime.now().date() + timedelta(days=6)
            auth_users[user][
                "FirstDate"] = f'{date.year}-{date.month}-{date.day}'
            auth_users[user][
                "LastDate"] = f'{date_week.year}-{date_week.month}-{date_week.day}'

            auth_users[user]["FirstParams"]["fromDatetime"] = f"{auth_users[user]['FirstDate']}T00:00:00.00"
            auth_users[user]["FirstParams"]["toDatetime"] = f"{auth_users[user]['LastDate']}T23:59:59.00"

            bot.send_message(call.message.chat.id,
                             f"✔️| <b>Информация принята</b>! \n📅| Записанная дата для фильтрации: \n <b>➤| Начало</b>:<i> {auth_users[user]['FirstDate']}</i>\n <b>➤| Конец</b>: <i>{auth_users[user]['LastDate']}</i>",
                             reply_markup=addMainButtons(user), parse_mode="html")
            bot.clear_step_handler_by_chat_id(user)

            bot.register_next_step_handler(call.message, clickButton)
        if call.data == "FastMonth":
            date = datetime.now().date()
            date_week = datetime.now().date() + timedelta(days=29)
            auth_users[user][
                "FirstDate"] = f'{date.year}-{date.month}-{date.day}'
            auth_users[user][
                "LastDate"] = f'{date_week.year}-{date_week.month}-{date_week.day}'

            auth_users[user]["FirstParams"]["fromDatetime"] = f"{auth_users[user]['FirstDate']}T00:00:00.00"
            auth_users[user]["FirstParams"]["toDatetime"] = f"{auth_users[user]['LastDate']}T23:59:59.00"

            bot.send_message(call.message.chat.id,
                             f"✔️| <b>Информация принята</b>! \n📅| Записанная дата для фильтрации: \n <b>➤| Начало</b>:<i> {auth_users[user]['FirstDate']}</i>\n <b>➤| Конец</b>: <i>{auth_users[user]['LastDate']}</i>",
                             reply_markup=addMainButtons(user), parse_mode="html")
            bot.clear_step_handler_by_chat_id(user)

            bot.register_next_step_handler(call.message, clickButton)
        if call.data == "CancelDate":
            sbros_Date(user)
            bot.send_message(call.message.chat.id,
                             "<b>💫| Отменил все текущие действия</b>. Выберите то, что Вас интересует:",
                             parse_mode="html", reply_markup=addMainButtons(user))
            bot.clear_step_handler_by_chat_id(user)
            bot.register_next_step_handler(call.message, clickButton)




    except:

        print("Error")


bot.polling(none_stop=True)
