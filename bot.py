import requests

import time

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHAT_ID = os.getenv("CHAT_ID")

LIMIT_MINUTES = 240  # 4 години

already_sent = False

def send_message(text):

    requests.get(

        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",

        params={

            "chat_id": CHAT_ID,

            "text": text

        }

    )

while True:

    try:

        data = requests.get(

            "https://back.echerha.gov.ua/api/v4/workload/1",

            timeout=30

        ).json()

        checkpoints = data["checkpoints"]

        chop = next(

            x for x in checkpoints

            if x["id"] == 17

        )

        wait_time = chop["wait_time"]

        vehicles = chop["vehicle_in_active_queues_counts"]

        if wait_time >= LIMIT_MINUTES and not already_sent:

            hours = round(wait_time / 60, 1)

            send_message(

                f"🚛 Чоп–Захонь\n"

                f"Черга перевищила 4 години.\n"

                f"Поточне очікування: {hours} год.\n"

                f"Авто в черзі: {vehicles}"

            )

            already_sent = True

        if wait_time < LIMIT_MINUTES:

            already_sent = False

    except Exception as e:

        print(e)

    time.sleep(900)
