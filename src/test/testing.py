import time
import logging, requests, timeit
import requests
import traceback as tb
from pprint import pp
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("PASSWORD")

data = {
    "login": f"Technopark",
    "password": password,
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

response = None
try:

    response = requests.post("https://test.vcc.uriit.ru/api/auth/login", json=data)

    token = response.json().get("token")

    headers = {
        "Authorization": f"Bearer {token}"
    }
    test = {
        "fromDatetime": "2024-08-06T00:00:00.00",
        "toDatetime": "2024-11-19T00:00:00.00",
        "state": None,
        "filter": None,
        "departmentId": 43,
        "userId": None,
        "priority": None

    }
    params = {
        "name": "Анали"
    }

    text = "kolosovym@uriit.ru, jeson.jesonov@gmail.com, babindj100@ya.ru"

    to_dict = list()
    with requests.Session() as session:
        # Устанавливаем заголовки для всех запросов через сессию
        session.headers.update(headers)

        # Обработка email-ов
        for email in text.split(","):
            time.sleep(5)

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
                    print("Iteration")
                    to_dict.append(
                        {
                            "id": i["id"],
                            "roleIds": i["roleIds"],
                            "departmentId": i["departmentId"],
                            "lastName": i["lastName"],
                            "firstName": i["firstName"],
                            "middleName": i["middleName"],
                        }
                    )
            else:
                print("Ошибка:", email.strip())

        # Выводим итоговые данные
        pp(to_dict)

    response_state = requests.get("https://test.vcc.uriit.ru/api/statistics/meetings-count", headers=headers)
    response_rooms = requests.get("https://test.vcc.uriit.ru/api/meetings", headers=headers, params=test)
    response_build = requests.get("https://test.vcc.uriit.ru/api/catalogs/rooms", headers=headers)
    response_buildings = requests.get("https://test.vcc.uriit.ru/api/catalogs/buildings", headers=headers)
    response_users = requests.get("https://test.vcc.uriit.ru/api/users", headers=headers)
    response_acc = requests.get("https://test.vcc.uriit.ru/api/account/user-info", headers=headers)


    if response_rooms:
        # pp(response_rooms.json())
        # test["userParticipant"] = response_acc.json()["id"]
        finalMsgLast = ""
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

            response_idroom = requests.get(f"https://test.vcc.uriit.ru/api/meetings/1069",
                                           headers=headers)
            # pp(response_idroom.json())
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
                "Название ВКС:": f'"{name}"',
                "Место проведения:": f"{field}",
                "Дата и время начала:": f"{createdAt.split('T')[0]}",
                "Продолжительность:": f"{dur}",
                "Организатор:": f"{orgUser}",
                "Участники:": "\n- " + '\n- '.join(participants),
                "Средство проведения:": f"{platform}",
            }

            text = ""
            for index, word in finalMsg.items():
                text = text + f"{index} {word}" + "\n"
            finalMsgLast = finalMsgLast + "\n" + "".join(text)
        if finalMsgLast:
            for i in range(0, len(finalMsgLast), 4096):
                pp(finalMsgLast[i:i + 4096])
        else:
            pp("По заданным параметрам ничего на найдено.")

    else:
        print(response_rooms.text, response_rooms)
except:
    tb.print_exc()
