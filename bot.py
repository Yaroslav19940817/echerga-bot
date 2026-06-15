import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Поріг у хвилинах (4 години)
LIMIT_MINUTES = 240

already_sent = False


def send_message(text):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )


while True:
    try:
        response = requests.get(
            "https://back.echerha.gov.ua/api/v4/workload/1",
            headers={
                "User-Agent": "Mozilla/5.0",
                "X-Client-Locale": "uk"
            },
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text[:500])

        response.raise_for_status()

        data = response.json()

        checkpoints = data["data"]

        chop = next(
            item for item in checkpoints
            if item["id"] == 17
        )

        wait_time = chop["wait_time"]
        vehicles = chop["vehicle_in_active_queues_counts"]

        print(
            f"Чоп-Захонь | wait_time={wait_time} хв | vehicles={vehicles}"
        )

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
        print("ERROR:", str(e))

    time.sleep(900)
