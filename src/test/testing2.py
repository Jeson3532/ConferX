import requests
import traceback as tb
from pprint import pp
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

data3 = {

    "id": None,
    "name": f"The VKSKK1",
    "comment": "",
    "participantsCount": f"5",
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
    "backend": f"fgfgfg",
    "sendNotificationsAt": 0,
    "startedAt": f"2024-11-15T18:00:00.000Z",
    "endedAt": None,
    "organizedBy": {
        "id": 543
    },
    "isGovernorPresents": False,
    "duration": 60,
    "isNotifyAccepted": False,
    "isVirtual": False,
    "recurrence": None,
    "participants": [
        {
            "id": 509,
            "lastName": "Тестовый",
            "firstName": "Для удаления",
            "middleName": "Пользователь",
            "roleIds": [],
            "departmentId": None,
            "email": "babindj100@ya.ru"
        },
        {
            "id": 543,
            "lastName": "Платинов",
            "firstName": "Никита",
            "middleName": "",
            "roleIds": [
                3
            ],
            "departmentId": 43,
            "email": "jeson.jesonov@gmail.com"
        }
    ],
    "attachments": [],
    "groups": []
}

data2 = {

    "id": None,
    "name": "New VKS 6",
    "roomId": 58,
    "comment": "",
    "participantsCount": "2",
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
    "backend": "fddfdf",
    "sendNotificationsAt": 0,
    "startedAt": "2024-11-15T18:00:00.000Z",
    "endedAt": None,
    "organizedBy": {
        "id": 543
    },
    "isGovernorPresents": False,
    "duration": 60,
    "isNotifyAccepted": False,
    "isVirtual": False,
    "recurrence": None,
    "participants": [
        {
            "id": 509,
            "lastName": "Тестовый",
            "firstName": "Для удаления",
            "middleName": "Пользователь",
            "roleIds": [],
            "departmentId": None,
            "email": "babindj100@ya.ru"
        },
        {
            "id": 543,
            "lastName": "Платинов",
            "firstName": "Никита",
            "middleName": "",
            "roleIds": [
                3
            ],
            "departmentId": 43,
            "email": "jeson.jesonov@gmail.com"
        }
    ],
    "attachments": [],
    "groups": []
}

test = {
    "fromDatetime": "2024-08-06T00:00:00.00",
    "toDatetime": "2024-11-19T00:00:00.00",
    "state": None,
    "filter": None,
    "departmentId": None,
    "userId": None,
    "priority": None
}

response = requests.post("https://test.vcc.uriit.ru/api/auth/login", json=data)

token = response.json().get("token")

headers = {
    "Authorization": f"Bearer {token}"
}

response_rooms = requests.get("https://test.vcc.uriit.ru/api/meetings/1020", headers=headers, params=test)
response_post = requests.post(f"https://test.vcc.uriit.ru/api/meetings", headers=headers, json=data3)
pp(type(data2))
pp(response_post)
pp(response_post.json())
# ➤, ▶, ➡ ━━━━━━━━━━ ➖➖➖ 🔔, 📌 ✅, ☑️, ✔️ ❌, ✖️ ⏰, 🕒 📅, 🗓️ 🔹 ⏰ ⏳ ♻️ 💫 ⚙️ 🔸|
